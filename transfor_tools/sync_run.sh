#! /bin/sh
PATH=/usr/local/sbin:/usr/bin:/usr/sbin:/sbin:/bin
# 脚本批量执行工具
# 并行执行
if [ $# -lt 4 ];then
    echo "Usage: $0 <ip|ip_list_file> <user> <password> <script_dir> [params]"
    echo -e "error\t1\tinput error"
	echo -e "\nToolResult\t0"
    exit 1
fi
echo "run pid is $$"

cd $(dirname $(which $0))

#并行执行数量
p_count=100
#每批IP执行完后等待时间
sleep_count=10

ip_list=$1
user=$2
password=$3
script_dir=`echo $4 | sed -e "s:/*$::g"`
params=$5
log_dir="./log/`basename $script_dir`_`date +%Y%m%d%H%M%S`"
mkdir -p $log_dir 2>/dev/null

### check tool file
if [ ! -f "$script_dir/cmd.sh" ];then
	echo -e "error\t1\tscript error"
	echo -e "\nToolResult\t0"
    exit 1
fi
### end tool file check

log()
{
    echo "[`date '+%Y-%m-%d %H:%M:%S'`] $*"
}

get_passwd()
{
#ret=`echo "select password from t_passwd_info where flag in (-2,0,1,2,3) and host='${1}' limit 1" | \
	ret=`echo "select password from t_passwd_info where host='${1}' limit 1" | \
    /usr/local/mysql/bin/mysql -uampsw -h172.27.3.212 passwd_manage -pmichael@tencent.com | sed '1d'`
}

get_user_passwd()
{
	ret=`/usr/sbin/systool/gpwd_user -u funnychen -p'chen1!@#' ${1}`
}

check_port()
{
    nc_cmd="/usr/bin/nc"
    if [ ! -f $nc_cmd ];then
        nc_cmd="/usr/bin/netcat"
    fi

    $nc_cmd -zn -w4 $1 $2
    if [ $? -ne 0 ];then
        for (( i=0 ; i<3 ; i++ ))
        do
            $nc_cmd -zn -w4 $1 $2
            if [ $? -eq 0 ];then return 0;fi
            sleep 1
        done
        return 1
    fi
    return 0
}

if [ ! -f "$ip_list" ];then
    expr "$ip_list" : "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}$" > /dev/null
    if [ $? -eq 0 ];then
        ips=$ip_list
    else
        exit 1
    fi
else
    ips=`cat $ip_list`
fi

count=0

ip_count=0

### autobat the ip list
for ip in $ips
do
    ip_count=$(( $ip_count + 1 ))
    echo ""
    echo "-------------------------正处理第 $ip_count 个IP [ $ip ]--------------------------"
    echo ""

    ip=`echo $ip|awk -F= '{print $NF}'`
    echo $ip
    if [ ! -z "`echo $ip | grep "NULL"`" ]
    then
	echo -e "AUTOBAT\t${ip}\t0\t1输入参数错误！"
        continue;
    fi

    #check_port $ip 36000
    #if [ $? -ne 0 ];then
    #    log "36000端口不可连"
    #    continue
    #fi

    # if [ "$user" = "root" ];then
    #     get_passwd $ip
    #     password=$ret
    # fi

    # if [ "$user" = "user_00" ];then
    #     get_user_passwd $ip
    #     password=$ret
    # fi

    if [ "$password" = "" ];then
        echo $ip 获取密码失败
        continue
    fi

    ./upload.exp $user $ip $password $script_dir /tmp/ >$log_dir/$ip.log 2>&1 && ./do_command.exp $user $ip "/tmp/`basename $script_dir`/cmd.sh $params" $password >> $log_dir/$ip.log 2>&1 &

    count=`expr $count + 1`
    if [ $count -eq $p_count ];then
		sleep $sleep_count
        count=0
    fi
done
