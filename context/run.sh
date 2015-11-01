#!/bin/bash
set +H  # switch off history expansion to protect '!'
echo "copy (select alert_on_change_id, command, output, common_threshold, email_address from alert_on_change) to '/tmp/alert_on_change.csv' delimiter '!'" | psql alert_on_change  # extract rows
IFS=$'\n'
rm -rf /tmp/mail
mkdir -p /tmp/mail
for item in $(cat /tmp/alert_on_change.csv)
do
	ID=$(cut -d! -f1 <(echo $item))
	COMMAND=$(cut -d! -f2 <(echo $item))
	# Take the old output, and replace the \n with spaces as per our comparison
	OLD_OUTPUT=$(cut -d! -f3 <(echo $item) | sed 's/\\n/ /g')
	COMMON_THRESHOLD=$(cut -d! -f4 <(echo $item))
	EMAIL_ADDRESS=$(cut -d! -f5 <(echo $item))
	NEW_OUTPUT=$(eval $COMMAND)
	# Diff old and new output, and extract the common words percentage
	COMMON=$(dwdiff -s <(echo $OLD_OUTPUT) <(echo $NEW_OUTPUT) 2>&1 > /dev/null | tail -1 | sed 's/.* \([0-9]\+\)..common.*/\1/') | sed 's/.*0 words.*/0/'
	echo ================================================================================
	echo $OLD_OUTPUT
	echo ================================================================================
	echo $NEW_OUTPUT
	echo ================================================================================
	echo $(dwdiff -s <(echo $OLD_OUTPUT) <(echo $NEW_OUTPUT))
	echo ================================================================================
	echo $COMMON
	echo ================================================================================
	echo $COMMON_THRESHOLD
	echo ================================================================================
	# If the common words percentage is less than the threshold, trigger an alert
	if [[ $COMMON -lt $COMMON_THRESHOLD ]]
	then
		echo "update alert_on_change set output = '$NEW_OUTPUT', last_updated=now()  where alert_on_change_id = $ID"
		echo "update alert_on_change set output = '$NEW_OUTPUT', last_updated=now()  where alert_on_change_id = $ID" | psql alert_on_change
		echo "<br/>Output of '$COMMAND' has less than $COMMON_THRESHOLD per cent in common with previous" >> /tmp/mail/${EMAIL_ADDRESS}
		echo "<br/>$(diff <(echo $OLD_OUTPUT) <(echo $NEW_OUTPUT))" >> /tmp/mail/${EMAIL_ADDRESS}
		echo "<br/>" >> /tmp/mail/${EMAIL_ADDRESS}
	else
		echo "update alert_on_change set last_updated=now() where alert_on_change_id = $ID" | psql alert_on_change
	fi
done
