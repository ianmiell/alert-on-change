#!/bin/bash
./build_test.sh --config configs/push_test.cnf && docker pull imiell/alert_on_change:test && ./run_test.sh
