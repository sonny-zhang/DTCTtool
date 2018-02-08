# DTCTtool
这是一款无视数据结构、无视数据库类型的数据库对比工具

使用环境依赖：

一，了解Python安装依赖包的人，可以使用以下方法：
Windows-Python 3.6+
cx_Oracle：查看cx_Oracle安装方法
pymssql：查看pymssql安装方法
pymysql：pip install pymysql
xlwt：pip install xlwt
xlrd：pip install xlrd
xlutils：查看xlutils安装方法

二，不知道如何安装Python依赖包，并且没有安装Python的人：
直接解压文件：/需要的安装包/Python36.zip
然后配置环境变量：PYTH   末尾添加解压的路径


测试是否可用：
在cmd进入到工具根目录，运行命令：python run.py 没有报错，开始使用

使用方法：
一，	在config文件夹里填写“config.ini”文件，配置连接数据库的信息            
（这只需要配置一次，用来连接数据库）

 
二，	在config文件夹里填写“sqlconfig.xls”文件，配置对比sql和对比字段顺序    
（一定要确认下SQL语句是否可用，对比参数是否准确）

三，	在cmd进入该目录运行：python run.py

四，	在results文件夹获得比对结果Excel文件                                
一个result.xls文件是一组对比数据的结果

性能要求：
1，	一组sql数据：10万行(一行16个字段)，占用内存：1G
2，	一组sql数据：25万行(一行16个字段)，占用内存：2.4G

根据自己的电脑去估算自己的使用量
