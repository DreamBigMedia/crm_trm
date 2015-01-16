#!/bin/bash
TIME=`date`
netstat -tlp | grep 55555
if [[ $? != 0 ]]; then cd /root/crm_trm/; screen -dmS orderapi python orderapi.py; echo "[ ${TIME} ] !!!!!!!!!!!!restarted order server!!!!!!!!!!!!">>order.log; mkdir orderdrops; cat order.log> orderdrops/crash`date +"%m_%d_%Y"`.log; else echo "order api server is live"; fi

netstat -tlp | grep 30303
if [[ $? != 0 ]]; then cd /root/crm_trm/; screen -dmS viewsapi python viewsapi.py; echo "[ ${TIME} ] !!!!!!!!!!!!restarted views server!!!!!!!!!!!!">>views.log; mkdir viewdrops; cat views.log> viewdrops/crash`date +"%m_%d_%Y"`.log; else echo "views api server is live"; fi

