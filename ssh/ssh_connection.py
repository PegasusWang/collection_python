#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko


class SSHConnection:
    """
    对paramiko进行封装，实现远程命令执行和文件上传下载
    """

    def __init__(self, host='192.168.12.68', port=22, username='root', pwd='123456'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
        self.__transport = self.connect()

    def connect(self):
        """
        连接Linux服务器
        :return: transport对象
        """
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        return transport

    def upload(self, local_path, target_path):
        """
        上传本地文件到服务器上
        :param local_path:本地计算机上的文件路径
        :param target_path:远程服务器上的文件路径
        :return:无
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        """
        将服务器上的文件下载到本地
        :param remote_path:远程服务器上的文件路径
        :param local_path:本地计算机上的文件路径
        :return: 无
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        """
        在服务器上执行shell命令
        :param command:要执行的命令
        :return:执行命令后的返回结果
        """
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read().decode("utf-8")
        print(result)
        return result

    def close(self):
        """
        关闭服务器连接
        :return: 无
        """
        self.__transport.close()


def main():
    ssh = SSHConnection(host="192.168.56.136", port=22, username="root", pwd="123456")
    ssh.cmd('ls -lah;cd /home/python/Desktop/prj/run.sh')  # 执行ls -lah命令,并执行run.sh脚本
    ssh.upload(r'C:\Users\liming\Desktop\python_projects\program\test\test.py', '/home/python/Desktop/1.py')  # 将本地的test.py文件上传到远端服务器的/home/python/Desktop目录下并改名为1.py
    ssh.download('/home/python/Desktop/1.py', 'testdownload.py')  # 将远端服务器的/home/python/Desktop目录下的1.p下载到本地的test目录下并改名为test.py
    ssh.close()  # 关闭连接


if __name__ == '__main__':
    main()
