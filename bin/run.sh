#!/bin/bash
# Example for running
DOCKER=${DOCKER:-docker}
IMAGE_NAME=imiell/alert_on_change
CONTAINER_NAME=alert_on_change
DOCKER_ARGS=''
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
${DOCKER} rm -f alert_on_change && ${DOCKER} run -d --name ${CONTAINER_NAME} ${DOCKER_ARGS} ${IMAGE_NAME}  /bin/sh -c '/root/start_postgres.sh && cron -f -L 8'
