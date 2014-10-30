#!/bin/bash

:<<EOF

Scan spp data from a specified ip list

Author: funnychen
Date: 2012-03-28

EOF

if [ $# != 1 ] || [ ! -f $1 ]; then
    echo "[`date +"%Y-%m-%d %H:%M:%S"`] $0 pid: $$, error: ip list not found"
	exit
fi

ip_list=$1
tool_path='/home/user_00/funnychen/AppSpp/tools'
get_ip_tool='/home/user_00/funnychen/AppSpp/crond/get_all_ip.php'

# Scan
echo "[`date +"%Y-%m-%d %H:%M:%S"`] $0 pid: $$, start to scan, total ip: `wc -l $ip_list | awk '{print $1}'`, ip list: $ip_list"
cd $tool_path
./sync_run.sh $ip_list user_00 'isd!@#user' tools/sppms_scan_no_sleep/

echo "[`date +"%Y-%m-%d %H:%M:%S"`] $0 pid: $$, finish"

