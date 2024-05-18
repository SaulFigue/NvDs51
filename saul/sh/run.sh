#!/bin/bash

cd /opt/nvidia/deepstream/deepstream-5.1/sources/apps/cc-lc/nvmsgconv
make install

cd /opt/nvidia/deepstream/deepstream-5.1/sources/apps/cc-lc/deepstream_test5
make install
./deepstream-test5-app -c configs/stadyn.txt
# > Ds_log.txt 2>&1 &

# PID=$!
# sleep 60
# echo "q" > /proc/$PID/fd/0
# sleep 2
# kill -SIGINT $PID
