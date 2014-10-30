#! /bin/sh
PATH=/usr/local/sbin:/usr/bin:/usr/sbin:/sbin:/bin
# 脚本批量执行工具
if [ $# -lt 3 ];then
    echo "Usage: $0 <ip|ip_list_file> <user> <password> "
    echo -e "error\t1\tinput error"
	echo -e "\nToolResult\t0"
    exit 1
fi
echo "run pid is $$"

cd $(dirname $(which $0))

ip_list=$1
user=$2
password=$3


log()
{
    echo "[`date '+%Y-%m-%d %H:%M:%S'`] $*"
}

get_passwd()
{
    ret=`echo "select password from t_passwd_info where flag in (-2,0,1,2,3) and host='${1}' limit 1" | \
    /usr/local/mysql/bin/mysql -uampsw -h172.27.3.212 passwd_manage -pmichael@tencent.com | sed '1d'`
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

    check_port $ip 36000
    if [ $? -ne 0 ];then
        log "36000端口不可连"
        continue
    fi

    # if [ "$user" = "root" ];then
    #     get_passwd $ip
    #     password=$ret
    # fi

    # if [ "$password" = "" ];then
    #     echo $ip 获取密码失败
    #     continue
    # fi

    #.sh download.exp user ip pwd src dst
    ./download.exp $user $ip $password "/usr/local/apache_2.0.59/conf/httpd.conf" ./waynewang/$ip.conf 2>&1
done

