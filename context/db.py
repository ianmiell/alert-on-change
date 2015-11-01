#!/usr/bin/python
import psycopg2
import psycopg2.extras
import commands
 
def main():
	conn_string = "host='localhost' dbname='alert_on_change' user='postgres' password='password'"
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
	# HERE IS THE IMPORTANT PART, by specifying a name for the cursor
	# psycopg2 creates a server-side cursor, which prevents all of the
	# records from being downloaded at once from the server.
	cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
	# execute our Query
	cursor.execute("select alert_on_change_id, command, output, common_threshold, email_address from alert_on_change")
 
	# Because cursor objects are iterable we can just call 'for - in' on
	# the cursor object and the cursor will automatically advance itself
	# each iteration.
	# This loop should run 1000 times, assuming there are at least 1000
	# records in 'my_table'
	for row in cursor:
		alert_on_change_id = row[0]
		command = row[1]
		output = row[2]
		common_threshold = row[3]
		email_address = row[4]
		new_output = commands.getstatusoutput(command)
		print alert_on_change_id
		print new_output
		print output
		cursor2 = conn.cursor()
		cursor2.execute("""update alert_on_change set output=%s, last_updated=now() where alert_on_change_id = %s""",(output,alert_on_change_id))
	# retrieve the records from the database
	records = cursor.fetchall()
 
 
if __name__ == "__main__":
	main()

