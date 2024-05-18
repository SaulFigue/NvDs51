#!/bin/bash
#screen -dmS ping2 ping 8.8.8.8

# sleep 10
cd /kafka_2.13-3.4.0
# Start the ZooKeeper service
screen -dmS zoo bin/zookeeper-server-start.sh config/zookeeper.properties

sleep 10

# Start the Kafka broker service
screen -dmS kaf bin/kafka-server-start.sh config/server.properties
