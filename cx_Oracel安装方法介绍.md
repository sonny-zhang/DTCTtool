# cx_Oracle安装方法  

> 把握一个中心，版本一致：python版本，oracle客户端的版本，cx_Oracle的版本  
64位的操作系统也是可以安装32位的开发环境。反之则不行！切记！  

> 三个注意点：  
版本位数对应，都是32位/64位；  
cx_Oracle和python版本对应，都是3.6；  
cx_Oracle和instantclient版本对应，都是11；   

## 一、打包好的安装方法：
> 目前没有上传，敬请期待
1. cx_Oracel安装：双击cx_Oracle-5.3-11g.win-amd64-py3.6-2.exe  
2. oracle 客户端：将这三个dll文件复制到的PY目录的Libs/site-packages文件夹下面  

文件下载路径：

## 二、通过网站下载安装：

1. cx_Oracel安装：下载低版本cx_Oracle版本 cx_Oracle-5.3-11g.win-amd64-py3.6-2.exe  
https://pypi.org/project/cx_Oracle/5.3/#files

> 不建议直接使用pip install cx_Oracle命令安装，因为版本问题容易报错。  
cx_Oracle 报错：cx_Oracle.DatabaseError: DPI-1050: Oracle Client library must be at version 11.2，这就是cx_Oracle版本太高引起的。  

2. oracle 客户端：下载的文件解压，复制oci，oraocci11，oraociei11的3个DLL粘贴到你的PY目录的Libs/site-packages文件夹下面   
http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html

## 测试是否安装成功：
import cx_Oracle  

conn = cx_Oracle.connect('用户名/密码@主机ip地址/orcl')  
# 用自己的实际数据库用户名、密码、主机ip地址 替换即可  
curs=conn.cursor()  
sql='SELECT * FROM 。。。' #sql语句  
rr=curs.execute (sql)  
row=curs.fetchone()  
print(row[0])  
curs.close()  
conn.close()  

群号：  
QQ：585499566