#!/usr/bin/python
import psycopg2
import psycopg2.extras
import commands
import argparse
import sys
import mailgun

# 1) For each line
# 2) run the command and collect the output
# 3) compare with what's there.
# 4) If it's the same, do nothing, if it's different (dwdiff -s)
# 5) update the db
# 6) send a mail

def main():
	parser = argparse.ArgumentParser()
	mail_run=True
	parser.add_argument('--test', help='Do not send emails or commit data', const=True, default=False, action='store_const')
	parser.add_argument('--insert_alert', help="""Insert alert as a dictionary, eg --insert_alert '{"command":"ls","email_address":"...}'.\nFields are:\n\tcommand\n\temail_address\n\tdescription\n\toutput\n\tcadence\n\tcommon_threshold\n\tignore_output\n\toutput\n\tfollow_on_command}'""",default='')
	args = parser.parse_args(sys.argv[1:])
	test = args.test
	insert_alert = args.insert_alert
	if insert_alert != '':
		mail_run=False
	if mail_run:
		send(test=test)
	elif insert_alert != '':
		import json
		insert_dict = json.loads(insert_alert)
		insert_row(insert_dict,test=test)
	
def insert_row(insert_dict,test=True):
	command           = insert_dict['command']
	email_address     = insert_dict['email_address']
	description       = insert_dict['description']
	cadence           = int(insert_dict['cadence'])
	common_threshold  = int(insert_dict['common_threshold'])
	# It's a buffer, so convert to string
	ignore_output     = insert_dict['ignore_output']
	output            = insert_dict['output']
	follow_on_command = insert_dict['follow_on_command']
	conn = _get_db_conn()
	cursor = conn.cursor()
	cursor.execute("insert into alert_on_change(command, common_threshold, email_address, description, cadence, ignore_output, output, follow_on_command) values(%s,%s,%s,%s,%s,%s,%s,%s)",(command,common_threshold,email_address,description,cadence,ignore_output.encode('latin-1'),output.encode('latin-1'),follow_on_command))
	if not test:
		conn.commit()
	cursor.close()

def _get_db_conn():	
	conn_string = "host='localhost' dbname='alert_on_change' user='postgres' password='password'"
	# get a connection, if a connect cannot be made an exception will be raised here
	return psycopg2.connect(conn_string)

def send(test=True):
	conn = _get_db_conn()
	# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
	# psycopg2 creates a server-side cursor, which prevents all of the
	# records from being downloaded at once from the server.
	cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
	# execute our Query
	cursor.execute("select alert_on_change_id, command, output, common_threshold, email_address, description, last_updated, cadence, ignore_output, ok_exit_codes, follow_on_command from alert_on_change")

	# Because cursor objects are iterable we can just call 'for - in' on
	# the cursor object and the cursor will automatically advance itself
	# each iteration.
	for row in cursor:
		alert_on_change_id = row[0]
		command            = row[1]
		output             = row[2]
		common_threshold   = row[3]
		email_address      = row[4]
		description        = row[5]
		last_updated       = row[6]
		cadence            = row[7]
		# Turn buffer into a string.
		ignore_output      = str(row[8])
		ok_exit_codes      = row[9]
		follow_on_command  = row[10]
		print 'command: ' + command
		print 'common_threshold: ' + str(common_threshold)
		print 'email_address: ' + email_address
		print 'description: ' + description
		print 'last_updated: '
		print last_updated
		print 'cadence: ' + str(cadence)
		print '================================================================================='
		print 'OLD OUTPUT:'
		print output
		print 'IGNORE OUTPUT:'
		print ignore_output
		print 'cadence: ' + str(cadence)
		print '================================================================================='
		#if current time in seconds - time last updated in seconds < cadence, then skip
		if False and int(time.time()) - int(last_updated) < cadence:
			print 'Cadence not breached, continuing'
			continue
		(status,new_output) = commands.getstatusoutput("""/bin/bash -c '""" + command + """'""")
		new_output = new_output.decode('latin_1')
		if status not in ok_exit_codes:
			print 'Status not returned ok! : ' + str(status)
			print 'Output: ' + new_output
			continue
		print '================================================================================='
		print 'NEW OUTPUT:'
		print new_output.encode('latin_1')
		print '================================================================================='
		print 'command run'
		if new_output == ignore_output:
			print 'Ignore output matched, continuing'
			continue
		f = open("new", "w")
		f.write(new_output.encode('latin_1'))
		f.close()
		f = open("old", "w")
		f.write(str(output))
		f.close()
		print 'files written'
		(status,dwdiff_output) = commands.getstatusoutput(r"""dwdiff old new""")
		(status,common_percent) = commands.getstatusoutput(r"""dwdiff -s old new 2>&1 > /dev/null | tail -1 | sed 's/.* \([0-9]\+\)..common.*/\1/' | sed 's/.*0 words.*/0/'""")
		common_percent = int(common_percent)
		(status,diff) = commands.getstatusoutput(r"""diff old new""")
		cursor2 = conn.cursor()
		if not test and common_percent < int(common_threshold):
				cursor2 = conn.cursor()
				cursor2.execute("""update alert_on_change set output=%s, last_updated=now() where alert_on_change_id = %s""",(new_output.encode('latin_1'),alert_on_change_id))
				if follow_on_command != '':
					(follow_on_status,follow_on_output) = commands.getstatusoutput("""/bin/bash -c '""" + follow_on_command + """'""")
				else:
					follow_on_output = ''
				mailgun.Mailgun.init("MAILGUNAPIUSER")
				mailgun.MailgunMessage.send_txt("MAILGUNADDRESS",email_address,'Alert on change triggered!','''Output of command described as: ''' + description + ''' has changed.

COMMAND:

''' + command + '''

FOLLOW-ON OUTPUT:

''' + follow_on_output + '''

WORD DIFF:

''' + dwdiff_output + '''

DIFF: 

''' + diff)
		commands.getoutput('rm -f new old')
		cursor2.close()
	cursor.close()
	if not test:
		conn.commit()


if __name__ == "__main__":
	main()

