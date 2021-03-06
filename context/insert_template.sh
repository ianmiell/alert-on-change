#!/bin/bash
set -x
echo 'input command'
read command
echo 'email_address'
read email_address
echo 'description'
read description
echo 'output (empty is ok)'
read output
echo 'cadence (empty is ok)'
read cadence
echo 'common_threshold (empty is ok)'
read common_threshold
echo 'ignore_output (empty is ok)'
read ignore_output
echo 'follow-on-command (empty is ok)'
read follow_on_command

if [[ $common_threshold = '' ]]
then
	common_threshold=100
fi
if [[ $cadence = '' ]]
then
	cadence=3600
fi
if [[ $output = '' ]]
then
	output=""
fi
if [[ $ignore_output = '' ]]
then
	ignore_output=""
fi
if [[ $follow_on_command = '' ]]
then
	follow_on_command=""
fi

for item in command email_address description
do
	if [[ $(eval echo \$$(echo $item)) = '' ]]
	then
		echo $item needs to be set
		exit 1
	fi
done

python db.py --insert_alert '{"command":"'"$command"'","email_address":"'"$email_address"'","description":"'"$description"'","output":"'"$output"'","cadence":"'"$cadence"'","common_threshold":"'"$common_threshold"'","ignore_output":"'"$ignore_output"'","follow_on_command":"'"$follow_on_command"'"}'
