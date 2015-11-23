#!/usr/bin/python
import psycopg2
import psycopg2.extras
import commands
import argparse
import sys

# 1) For each line
# 2) run the command and collect the output
# 3) compare with what's there.
# 4) If it's the same, do nothing, if it's different (dwdiff -s)
# 5) update the db
# 6) send a mail

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--test', help='Do not send emails', const=True, default=False, action='store_const')
	args = parser.parse_args(sys.argv[1:])
	test = args.test

	conn_string = "host='localhost' dbname='alert_on_change' user='postgres' password='password'"
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
	# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
	# psycopg2 creates a server-side cursor, which prevents all of the
	# records from being downloaded at once from the server.
	cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
	# execute our Query
	cursor.execute("select alert_on_change_id, command, output, common_threshold, email_address, description, last_updated, cadence from alert_on_change")

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
		print '================================================================================='
		#if current time in seconds - time last updated in seconds < cadence, then skip
		if False and int(time.time()) - int(last_updated) < cadence:
			continue
		new_output = commands.getoutput(command).decode('latin_1')
		print 'command run'
		f = open("new", "w")
		f.write(new_output.encode('latin_1'))
		f.close()
		f = open("old", "w")
		f.write(str(output))
		f.close()
		print 'files written'
		common_percent = int(commands.getoutput(r"""dwdiff -s old new 2>&1 > /dev/null | tail -1 | sed 's/.* \([0-9]\+\)..common.*/\1/' | sed 's/.*0 words.*/0/'"""))
		cursor2 = conn.cursor()
		if not test:
			if common_percent < int(common_threshold):
				cursor2 = conn.cursor()
				cursor2.execute("""update alert_on_change set output=%s, last_updated=now() where alert_on_change_id = %s""",(new_output.encode('latin_1'),alert_on_change_id))
				commands.getoutput('''echo 'Output of command described as: ''' + description + ''' has changed.' > /tmp/email_content''')
				commands.getoutput('''curl -s --user "MAILGUNAPIUSER"  https://api.mailgun.net/v3/sandbox8bf98fb559c041779511cb4e546e5347.mailgun.org/messages -F from='Alert On Change <mailgun@sandbox8bf98fb559c041779511cb4e546e5347.mailgun.org>'  -F to=''' + email_address + ''' -F subject='Alert on change triggered!' -F text="$(cat /tmp/email_content)"''')
				#commands.getoutput('''cat /tmp/email_content | mail -s "alert" --debug-level=100 ''' + email_address)
				print commands.getoutput('''echo ================================================================================''')
				print commands.getoutput('''cat email_content''')
				print commands.getoutput('''echo ================================================================================''')
				print commands.getoutput('''cat old''')
				print commands.getoutput('''echo ================================================================================''')
				print commands.getoutput('''cat new''')
				print commands.getoutput('''echo ================================================================================''')
		commands.getoutput('rm -f new old email_content')
	conn.commit()


if __name__ == "__main__":
	main()

