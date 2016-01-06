#!/bin/bash
./build_test.sh --config configs/push_test.cnf -s shutit.alert_on_change.alert_on_change.alert_on_change testing true && docker pull imiell/alert_on_change:test && ./run_test.sh
