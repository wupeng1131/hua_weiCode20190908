#!/bin/bash
team_id=$1
server_ip=$2
server_port=$3
cd "$(dirname "$0")"
cd jar
java -jar demo.jar $team_id $server_ip $server_port

