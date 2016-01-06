#!/bin/bash
set -x
set -e
rm -rf /tmp/alert-on-change-checkout
mkdir -p /tmp/alert-on-change-checkout
cd /tmp/alert-on-change-checkout
git clone --recursive https://github.com/ianmiell/alert-on-change > /tmp/alert_on_change 2>&1 
cd alert-on-change/bin && PATH=${PATH}:/space/git/shutit ./build.sh --config configs/push.cnf >> /tmp/alert_on_change 2>&1 
PATH=${PATH}:/space/git/shutit ./run.sh >> /tmp/alert_on_change 2>&1
