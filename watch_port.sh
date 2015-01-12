#!/bin/bash
netstat -lp | grep 55555
if [[ $? != 0 ]]; then screen -d -m -L -S autorestart "cd /root/crm_trm/ && python orderapi.py"; fi
