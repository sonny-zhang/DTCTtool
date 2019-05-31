# DTCTtool
这是一款无视数据结构、无视数据库类型的数据库对比工具  
目前支持的数据库类型：Oracle，SqlServer  

## 使用环境依赖：  
> cx_Oracle 、pymssql这两个包使用pip安装会报使用错误，请看文档安装

cx_Oracle：查看cx_Oracle安装使用方法.md  
pymssql：查看pymssql安装方法介绍.md  
xlwt：pip install xlwt  
xlrd：pip install xlrd  
xlutils：查看网上xlutils安装方法  

## 测试是否可用：  

在cmd进入到工具根目录，运行命令：python run.py 没有报错，开始使用

## 使用方法：

一，在config文件夹里填写“config.ini”文件，配置连接数据库的信息  
> （这只需要配置一次，用来连接数据库）

这是“config.ini”文件
![image](https://github.com/sonny-zhang/DTCTtool/blob/master/image/config.png)

二，在config文件夹里填写“sqlconfig.xls”文件，配置对比sql和对比字段顺序  
> （一定要确认下SQL语句是否可用，对比参数是否准确）

这是“sqlconfig.xls”文件
![image](https://github.com/sonny-zhang/DTCTtool/blob/master/image/sqlconfig.png)

三，在cmd进入该目录运行：python run.py

四，在results文件夹获得比对结果Excel文件                                
> 一个result.xls文件是一组对比数据的结果

这是“result.xls”文件
![image](https://github.com/sonny-zhang/DTCTtool/blob/master/image/config.png)

五，对于一组大型数据的sql，根据性能要求可以进行拆分：  
    拆分后的一组sql要保证，大多数的主键(或联合主键)是相同的，否则这组sql就是无效，获得的results文件所有的数据都是异常对比数据

## 性能要求：

1，	一组sql数据：10万行(一行16个字段)，占用内存：1G  
2，	一组sql数据：25万行(一行16个字段)，占用内存：2.4G  
根据自己的电脑去估算自己的使用量

群号：  
QQ：585499566
