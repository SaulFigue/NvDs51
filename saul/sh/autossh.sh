#!/bin/bash

cd /opt/nvidia/deepstream/deepstream-5.1

# Start a tunel with autossh
screen -dmS tunel autossh -N -i ./OMIA_key.pem -L 10001:localhost:5432 omia@20.102.54.12
