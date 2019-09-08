#!/bin/bash
cd "$(dirname "$0")"
cd client
TIMESTAMP=`date +"%Y-%m-%d_%H-%M-%S"`
LOGFILE=/var/log/battle-peng-$TIMESTAMP.log
touch $LOGFILE

sh start.sh $1 $2 $3 > $LOGFILE
