"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class alert_on_change(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		#
		shutit.install('curl git dwdiff html2text python-psycopg2 sudo cron expect wget python-dev python-pip')
		shutit.send('pip install simplejson')
		shutit.send('pip install mailgun')
		shutit.send('groupadd -g 1000 alertonchange')
		shutit.send('useradd -g alertonchange -d /home/alertonchange -s /bin/bash -m alertonchange')
		shutit.send('adduser alertonchange sudo')
		shutit.send('echo "%sudo ALL=(ALL:ALL) ALL" > /etc/sudoers.d/sudo')
		shutit.send('chmod 0440 /etc/sudoers.d/sudo')
		shutit.login('postgres')
		shutit.send('git config --global user.email ' + shutit.cfg[self.module_id]['git_email'])
		shutit.send('git config --global user.name ' + shutit.cfg[self.module_id]['git_name'])
		shutit.send('git clone https://github.com/ianmiell/alert-on-change.git')
		shutit.send('cd alert-on-change')
		shutit.send('echo create database alert_on_change | psql postgres')
		shutit.send('psql alert_on_change < context/SCHEMA.sql')
		shutit.send('psql alert_on_change < context/DATA.sql')
		shutit.send('''echo "alter user postgres password 'password'" | psql postgres''')
		shutit.send('createuser -s alertonchange')
		shutit.send('''echo "alter user alertonchange with password 'postgres'" | psql postgres''')
		shutit.logout()
		shutit.login('alertonchange')
		shutit.send_host_file('/tmp/db.py','context/db.py')
		shutit.send('''sed -i 's/MAILGUNAPIUSER/''' + shutit.cfg[self.module_id]['mailgunapiuser'] + '''/g' /tmp/db.py''')
		shutit.send('''sed -i 's/MAILGUNADDRESS/''' + shutit.cfg[self.module_id]['mailgunapiuser'] + '''/g' /tmp/db.py''')
		shutit.send("""echo "* * * * * python /tmp/db.py" | crontab -u alertonchange -""")
		shutit.logout()
		shutit.login('postgres')
		shutit.send('cd alert-on-change')
		shutit.send(r"""echo "5,25,45 * * * * cd alert-on-change && pg_dump alert_on_change -a > context/DATA.sql && pg_dump alert_on_change -s > context/SCHEMA.sql && git commit -am 'latest backup' && /tmp/push.exp" | crontab -u postgres -""")
		shutit.send_file('/tmp/push.exp',r'''#!/usr/bin/env expect
set timeout 100
spawn bash
send "git push origin master\n"
expect -re {sername}
send "''' + shutit.cfg[self.module_id]['git_username'] + r'''\n"
expect -re {assword}
send "''' + shutit.cfg[self.module_id]['git_password'] + r'''\n"
expect -re {postgres}''')
		shutit.send('chmod +x /tmp/push.exp')
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		shutit.get_config(self.module_id, 'git_name')
		shutit.get_config(self.module_id, 'git_email')
		shutit.get_config(self.module_id, 'git_username')
		shutit.get_config(self.module_id, 'git_password')
		shutit.get_config(self.module_id, 'testing', boolean=True, default=False)
		shutit.get_config(self.module_id, 'mailgunapiuser')
		shutit.get_config(self.module_id, 'mailgunaddress')
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		shutit.send('python /tmp/db.py --test')
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return alert_on_change(
		'shutit.alert_on_change.alert_on_change.alert_on_change', 1801706206.00,
		description='',
		maintainer='',
		delivery_methods=['docker'],
		depends=['shutit.tk.postgres.postgres']
	)

