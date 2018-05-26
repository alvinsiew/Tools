#/bin/bash
#
# Description: Script for housekeeping sftp files.
#
########################################################################################

sftp_path=/path/test
dir_list=/tmp/dir_list.lst
sftp_adr=192.168.1.123
sftp_user=centos
housekeep_days=5


# SFTP function
sftp_fuc()
{
sftp ${sftp_user}@${sftp_adr} 1> $dir_list << EOF
cd $sftp_path
$1
quit
EOF
}

# Date to exclude from cleaing.
exclude_opts()
{
cat $dir_list | awk '{print $6,$7}' | uniq | grep -v -e '^[[:space:]]*$' | tail -${housekeep_days}
}


# Connect to sftp server to list the files to be clean.
echo "Connecting to sftp server to list files to be clean."
sftp_fuc "ls -ltr"

opts=`exclude_opts`

sed -i '/sftp/d' "$dir_list"

# Remove files that does not need to be clean from list file.
while read line
do
    sed -i "/${line}/d" "$dir_list"
done  <<< "$opts"

del_file=`cat $dir_list | awk '{print $9}'`

# Clean files
echo "Connecting to sftp server for cleaning."
sftp_cmd=`for r in $del_file
do
	echo "rm $r" 
done`

sftp_fuc "${sftp_cmd}"

if [ $? == 0 ]; then
echo "Files clean successfully."
else
echo "Error cleaing files"
fi

rm -f $dir_list

