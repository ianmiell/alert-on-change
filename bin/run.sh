#!/bin/bash
# Example for running
DOCKER=${DOCKER:-docker}
IMAGE_NAME=imiell/alert_on_change
CONTAINER_NAME=alert_on_change
DOCKER_ARGS=''
ALERT_ON_CHANGE_FORM_PORT=${ALERT_ON_CHANGE_FORM_PORT:-9080}
while getopts "i:c:a:" opt
do
	case "$opt" in
	i)
		IMAGE_NAME=$OPTARG
		;;
	c)
		CONTAINER_NAME=$OPTARG
		;;
	a)
		DOCKER_ARGS=$OPTARG
		;;
	esac
done
(${DOCKER} rm -f ${CONTAINER_NAME} || /bin/true) && ${DOCKER} pull ${IMAGE_NAME} && ${DOCKER} run -d --name ${CONTAINER_NAME} ${DOCKER_ARGS} -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker:/var/lib/docker -p ${ALERT_ON_CHANGE_FORM_PORT}:8080 ${IMAGE_NAME} /bin/sh -c '/root/start_postgres.sh && (cd /home/alertonchange/alert-on-change/context/forms && sudo -u alertonchange python hn_insert.py &) && cron -f -L 8'
