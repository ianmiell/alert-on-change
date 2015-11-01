#!/bin/bash
for email_address in $(ls /tmp/mail)
do
	echo $(cat /tmp/mail/$email_address) | mail  -s "alert" --debug-level=100 $email_address
done
