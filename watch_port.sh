#!/bin/bash
netstat -p | grep 55555
if [[ $? != 0 ]]; then screen -d -m -L -S autorestart "cd /root/crm_trm/ && python orderapi.py"; echo "restarted server"; else echo "server is live"; fi
