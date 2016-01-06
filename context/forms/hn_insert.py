#!/usr/bin/python
import web
from web import form
import psycopg2
import psycopg2.extras
import mailgun
import random

render = web.template.render('templates/')
web.config.debug = False

urls = (
	'/', 'index',
	'/confirm/(.+)', 'confirm',
	'/confirm_ok/(.+)', 'confirm_ok',
	'/unsubscribe/(.+)', 'unsubscribe'
)
app = web.application(urls, globals())

def insert_row(insert_dict):
	command           = 'wget -qO- https://news.ycombinator.com/ | html2text | grep -i ' + insert_dict['command'] + ' | wc -l'
	email_address     = insert_dict['email_address']
	description       = insert_dict['description']
	cadence           = 600
	common_threshold  = 100
	# It's a buffer, so convert to string
	ignore_output     = ''
	output            = ''
	follow_on_command = 'wget -qO- https://news.ycombinator.com/ | html2text | grep -i ' + insert_dict['command']
	random_key        = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(8))
	conn = _get_db_conn()
	cursor = conn.cursor()
	cursor.execute("insert into alert_on_change(command, common_threshold, email_address, description, cadence, ignore_output, output, follow_on_command, random_key) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(command,common_threshold,email_address,description,cadence,ignore_output.encode('latin-1'),output.encode('latin-1'),follow_on_command,random_key))
	conn.commit()
	cursor.close()
	# send confirmation mail to user
	mailgun.Mailgun.init("MAILGUNAPIUSER")
	mailgun.MailgunMessage.send_txt("MAILGUNADDRESS",email_address,'Hacker News New Alert Confirmation','''Please confirm your email address: http://hnalert.tk/confirm/''' + random_key)

def _get_db_conn():	
	conn_string = "host='localhost' dbname='alert_on_change' user='postgres' password='password'"
	# get a connection, if a connect cannot be made an exception will be raised here
	return psycopg2.connect(conn_string)

myform = form.Form(
	form.Textarea("string",description='String to look for (case-insensitive), eg: "bitcoin"'),
	form.Textbox("email_address",description='email address to send alert to.'),
	form.Textarea("description",description='Description of what this is for.'),
) 


class index: 
	def GET(self): 
		form = myform()
		# make sure you create a copy of the form by calling it (line above)
		# Otherwise changes will appear globally
		return render.form(form)

	def POST(self): 
		form = myform() 
		if not form.validates(): 
			return render.form(form)
		else:
			insert_dict={}
			insert_dict['command']           = form.d.string
			insert_dict['email_address']     = form.d.email_address
			insert_dict['description']       = form.d.description
			insert_row(insert_dict)
			return render.success(form.d.email_address)

class confirm:
	def GET(self,random_key):
		conn = _get_db_conn()
		cursor = conn.cursor()
		cursor.execute("select alert_on_change_id, command from alert_on_change where random_key = %s",(random_key,))
		all_rows = cursor.fetchall()
		if len(all_rows) == 0:
			conn.commit()
			cursor.close()
			return 'USER NOT FOUND'
		if len(all_rows) > 1:
			conn.commit()
			cursor.close()
			return 'ERROR'
		command = all_rows[0][1]
		cursor.execute("update alert_on_change set status = 'R' where random_key = %s and status = 'P'",(random_key,))
		conn.commit()
		cursor.close()
		mailgun.Mailgun.init("MAILGUNAPIUSER")
		mailgun.MailgunMessage.send_txt("MAILGUNADDRESS",'ian.miell@gmail.com','New Alert Confirmation',"""Command is: """ + command + """

http://hnalert.tk/confirm_ok/""" + random_key)
		return render.success_confirm()


class confirm_ok:
	def GET(self,random_key):
		conn = _get_db_conn()
		cursor = conn.cursor()
		cursor.execute("select alert_on_change_id, command from alert_on_change where random_key = %s",(random_key,))
		all_rows = cursor.fetchall()
		if len(all_rows) == 0:
			conn.commit()
			cursor.close()
			return 'USER NOT FOUND'
		if len(all_rows) > 1:
			conn.commit()
			cursor.close()
			return 'ERROR'
		cursor.execute("update alert_on_change set status = 'A' where random_key = %s and status = 'R'",(random_key,))
		conn.commit()
		cursor.close()
		return render.success_confirm_ok()


class unsubscribe:
	def GET(self,random_key):
		conn = _get_db_conn()
		cursor = conn.cursor()
		cursor.execute("select alert_on_change_id from alert_on_change where random_key = %s",(random_key,))
		all_rows = cursor.fetchall()
		if len(all_rows) == 0:
			conn.commit()
			cursor.close()
			return 'USER NOT FOUND'
		if len(all_rows) > 1:
			conn.commit()
			cursor.close()
			return 'ERROR'
		cursor.execute("update alert_on_change set status = 'U' where random_key = %s",(random_key,))
		conn.commit()
		cursor.close()
		return render.success_unsubscribed()

if __name__=="__main__":
	web.internalerror = web.debugerror
	app.run()
