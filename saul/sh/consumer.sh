#!/bin/bash

# Python consumer to insert in Database lc-counting
cd /opt/nvidia/deepstream/deepstream-5.1/sources/apps/cc-lc/deepstream_test5
python3 consumer_saul2.py > consumer_log.txt 2>&1
