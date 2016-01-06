#!/usr/bin/python
import web
from web import form
import psycopg2
import psycopg2.extras

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

def insert_row(insert_dict):
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
	conn.commit()
	cursor.close()

def _get_db_conn():	
	conn_string = "host='localhost' dbname='alert_on_change' user='postgres' password='password'"
	# get a connection, if a connect cannot be made an exception will be raised here
	return psycopg2.connect(conn_string)

#	form.Textarea("command",pre='Command to run, eg: "wget -qO- https://news.ycombinator.com/ | grep -i mywidget'),
#	form.Textbox("email_address",post='email address to send alert to.'),
#	form.Textarea("description",post='Description of what this is for.'),
#	form.Textbox("cadence", form.notnull, form.regexp('\d+', 'Must be a digit'), form.Validator('Must be more than 60', lambda x:int(x)>60), value='600', post='Frequency of check, in seconds.'),
#	form.Textbox("common_threshold", form.notnull, form.regexp('\d+', 'Must be a digit'), form.Validator('Must be more than 0', lambda x:int(x)>0), form.Validator('Must be less than or equal to 100', lambda x:int(x)<=100), value='100', post='Percentage of common words below which an alert is triggered, eg if 100==alert if there is any change in output, 0==never send an alert.'),
#	form.Textbox('ignore_output',post='If the output matches this string, then do not alert.'),
#	form.Textarea('follow_on_command',post='If an alert is sent, then include the output of this command in the alert.')
myform = form.Form(
	form.Textarea("command",description='Command to run, eg curl http://myservice.com'),
	form.Textbox("email_address",description='email address to send alert to.'),
	form.Textarea("description",description='Description of what this is for.'),
	form.Textbox("cadence", form.notnull, form.regexp('\d+', 'Must be a digit'), form.Validator('Must be more than 60', lambda x:int(x)>60), value='600', description='Frequency of check, in seconds.'),
	form.Textbox("common_threshold", form.notnull, form.regexp('\d+', 'Must be a digit'), form.Validator('Must be more than 0', lambda x:int(x)>0), form.Validator('Must be less than or equal to 100', lambda x:int(x)<=100), value='100', description='% change+ triggers alert (0-100)'),
	form.Textbox('ignore_output',description='Ignore this output if seen.'),
	form.Textarea('follow_on_command',description='Include output of this command in alert.')
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
			insert_dict['command']           = form.d.command
			insert_dict['email_address']     = form.d.email_address
			insert_dict['description']       = form.d.description
			insert_dict['cadence']           = int(form.d.cadence)
			insert_dict['common_threshold']  = int(form.d.common_threshold)
			insert_dict['ignore_output']     = form.d.ignore_output
			insert_dict['output']            = ''
			insert_dict['follow_on_command'] = form.d.follow_on_command
			insert_row(insert_dict)
			return 'OK'
			#return "Grrreat success! boe: %s, bax: %s" % (form.d.boe, form['bax'].value)

if __name__=="__main__":
	web.internalerror = web.debugerror
	app.run()
