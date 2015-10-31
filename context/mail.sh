#!/bin/bash
for email_address in $(ls /tmp/mail)
do
	echo $(cat /tmp/mail/$email_address) | mail  -s "alert" $email_address
done
