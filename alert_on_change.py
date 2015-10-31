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
		shutit.install('mailutils')
		shutit.install('ssmtp')
		shutit.install('curl')
		shutit.install('git')
		shutit.install('dwdiff')
		shutit.install('html2text')
		shutit.login('postgres')
		shutit.send('curl https://raw.githubusercontent.com/docker-in-practice/docker-mailer/master/mail.sh > mail.sh')
		shutit.send('chmod +x mail.sh')
		shutit.send('git config --global user.email ' + shutit.cfg[self.module_id]['git_email'])
		shutit.send('git config --global user.name ' + shutit.cfg[self.module_id]['git_name'])
		shutit.send('git clone https://github.com/ianmiell/alert-on-change.git')
		shutit.send('cd alert-on-change')
		shutit.send('echo create database alert_on_change | psql postgres')
		shutit.send('psql alert_on_change < context/SCHEMA.sql')
		shutit.send('psql alert_on_change < context/DATA.sql')
		# 1) For each line
		# 2) run the command and collect the output
		# 3) compare with what's there.
		# 4) If it's the same, do nothing, if it's different (dwdiff -s)
		# 5) update the db
		# 6) send a mail
		shutit.send('''echo "copy (select alert_on_change_id, command, output, common_threshold, email_address from alert_on_change) to '/tmp/alert_on_change.csv' delimiter '!'" | psql alert_on_change''')
		shutit.send_host_file('/tmp/run.sh','context/run.sh')
		shutit.send('chmod +x /tmp/run.sh')
		shutit.send('/tmp/run.sh')
		shutit.pause_point('')
		shutit.send('pg_dump alert_on_change -a > context/DATA.sql')
		shutit.send('pg_dump alert_on_change -s > context/SCHEMA.sql')
		shutit.send("git commit -am 'latest backup'",check_exit=False)
		shutit.send('git push origin master',expect='sername')
		shutit.send(shutit.cfg[self.module_id]['git_username'],expect='assword')
		shutit.send(shutit.cfg[self.module_id]['git_password'])
		shutit.pause_point('')
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
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
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

