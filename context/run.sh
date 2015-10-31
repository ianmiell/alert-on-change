#!/bin/bash
IFS=$'\n'
rm -rf /tmp/mail
mkdir -p /tmp/mail
for item in $(cat /tmp/alert_on_change.csv)     
do    
    ID=$(cut -d, -f1 <(echo $item)) 
    COMMAND=$(cut -d, -f2 <(echo $item))  
    OLD_OUTPUT=$(cut -d, -f3 <(echo $item))     
    COMMON_THRESHOLD=$(cut -d, -f4 <(echo $item))     
    EMAIL_ADDRESS=$(cut -d, -f5 <(echo $item))  
    NEW_OUTPUT=$(eval $COMMAND)     
    COMMON=$(dwdiff -s <(echo $OLD_OUTPUT) <(echo $NEW_OUTPUT) 2>&1 > /dev/null | tail -1 | sed 's/.* \([0-9]\+\)..common.*/\1/')   
    #echo $OLD_OUTPUT   
    #echo $NEW_OUTPUT   
    #echo $(dwdiff -s <(echo $OLD_OUTPUT) <(echo $NEW_OUTPUT))    
    #echo $COMMON 
    #echo $COMMON_THRESHOLD   
    if [[ $COMMON -lt $COMMON_THRESHOLD ]];     
    then    
        echo "update alert_on_change set output = '$NEW_OUTPUT', last_updated=now()  where alert_on_change_id = $ID" | psql alert_on_change     
        echo "Output of '$COMMAND' has less than $COMMON_THRESHOLD per cent in common with previous" >> /tmp/mail/${EMAIL_ADDRESS}  
    fi
done
