import paramiko, sys, os, time, datetime


host = '192.168.1.180'
port = 22
transport = paramiko.Transport((host, port))
username = "centos"
key_file = '/Users/john/.ssh/id_rsa.pem'
sftp_path = "path/test/"

my_key = paramiko.RSAKey.from_private_key_file(key_file)
transport.connect(username = username, pkey=my_key)
paramiko.util.log_to_file("filename.log")

sftp = paramiko.SFTPClient.from_transport(transport)
print 'SFTP connection initiated'

for file in sftp.listdir(sftp_path):
    fullpath   = os.path.join(sftp_path,file) 
    timestamp = sftp.stat(fullpath).st_atime
    createtime = datetime.datetime.now()
    now = time.mktime(createtime.timetuple())
    datetime.timedelta = now - timestamp
    days =  datetime.timedelta // 86400

    if days  > 1:
        print("Deleting %s " % file)
        sftp.remove(fullpath)

sftp.close()
transport.close()
