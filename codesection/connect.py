from codesection.sqlconfig import Aconfig,Bconfig
import pymysql as mysql
import cx_Oracle as oracle
import pymssql as sqlserver
import configparser as config
import os, sys, gc


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'    #Oracle查询出的数据，中文输出问题解决
# f = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# ff = os.path.join(f, 'config','config.ini')
# file = ff.replace('\\', '/')
# cfg = config.ConfigParser()           # 创建一个管理对象cfg
# cfg.read(file, encoding='utf-8')  # 把ini文件读到cfg中

def ini():
    f = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    ff = os.path.join(f, 'config', 'config.ini')
    file = ff.replace('\\', '/')
    cfg = config.ConfigParser()  # 创建一个管理对象cfg
    try:
        cfg.read(file, encoding='utf-8')  # 把ini文件读到cfg中
        return cfg
    except Exception as e:
        print('ERROR：config.ini配置文件读取失败')
        sys.exit(1)


cfg = ini()

# 连接数据库：cfg(config对象管理器),db(ini配置数据库名)
def connect(db):
    if db[0:5] == 'MYSQL':
        db_host = cfg.get(db, 'db_host')
        db_port = cfg.get(db, 'db_port')
        db_user = cfg.get(db, 'db_user')
        db_pwd  = cfg.get(db, 'db_pwd')
        db_dbname = cfg.get(db, 'db_dbname')
        try:
            conn = mysql.connect(host=db_host, user=db_user, password=db_pwd, database=db_dbname)
            cursor = conn.cursor()
            sql = 'select version()'
            cursor.execute(sql)
            data = cursor.fetchone()
            return True
        except Exception as e:
            print (e)
            #return False

    elif db[0:6] == 'ORACLE':
        db_host = cfg.get(db, 'db_host')
        db_user = cfg.get(db, 'db_user')
        db_port = cfg.get(db, 'db_port')
        db_pwd  = cfg.get(db, 'db_pwd')
        db_sid  = cfg.get(db, 'db_sid')
        try:
            conn = oracle.connect(db_user+'/'+db_pwd+'@'+db_host+'/'+db_sid)
            cursor = conn.cursor()
            sql = 'select * from v$version'
            cursor.execute(sql)
            data = cursor.fetchone()
            print("%s连接成功:" % (db))
            #print ("数据库版本号为：%s"%(data))
            return conn
        except Exception as e:
            print ('%s连接失败：'%(db[0:6]))
            print ('Error:',e)
            sys.exit(1)
            return False

    elif db[0:9]  == 'SQLSERVER':
        db_host = cfg.get(db, 'db_host')
        db_port = cfg.get(db, 'db_port')
        db_user = cfg.get(db, 'db_user')
        db_pwd  = cfg.get(db, 'db_pwd')
        db_dbname = cfg.get(db, 'db_dbname')
        charset = cfg.get('DATA', 'charset')
        try:
            conn = sqlserver.connect(host=db_host, port=db_port, user=db_user, password=db_pwd, database=db_dbname)
            cursor = conn.cursor()
            sql = 'select @@version'
            cursor.execute(sql)
            data = cursor.fetchone()
            print ("%s连接成功:"%(db))
            #print ("数据库版本号为：%s"%(data))
            return conn
        except Exception as e:
            print ('%s连接失败：'%(db[0:9]))
            print ('Error:',e)
            sys.exit(1)

def source():
    sou = cfg.get('DATA', 'source')
    return sou

def target():
    tar = cfg.get('DATA', 'target')
    return tar

#获得对比数据:cfg(config对象管理器),db(ini配置数据库名)调用connect需要使用,sql(单条SQL语句)
def getdataA(sql):
    source = cfg.get('DATA', 'source')
    conn = connect(source)
    cursor = conn.cursor()
    try:
        #print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        #print(len(data),data)
        if len(data)==1:
            print('ERROE:','sql没有查询权限')
            sys.exit(1)
        else:
            #print('A原始数据获得成功')
            del source,cursor,sql
            gc.collect()
            return data
    except Exception as e:
        print('ERROR:源端SQL无效，请仔细看看SQL呦...',e)
    finally:
        conn.close()

def getdataB(sql):
    target = cfg.get('DATA', 'target')
    conn = connect(target)
    cursor = conn.cursor()
    try:
        #print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        # print (data)
        # print(len(data),type(data))
        if len(data)==1:
            print('ERROR:','sql没有查询权限')
            return False
        else:
            #print('B原始数据获得成功')
            return data
    except Exception as e:
        print('ERROR:目标端SQL无效，请仔细看看SQL呦...',e)
    finally:
        conn.close()

def test():
    sqlA = Aconfig()[0]
    sqlB = Bconfig()[0]
    ex = []
    for i in range(len(sqlA)):
        print('第%d组SQL连接测试：开始' % (i + 1))
        dataa = getdataA(sqlA[i])
        if dataa is not None:
            print('源端SQL连接测试：成功')
        else:
            ex.append(1)
        datab = getdataB(sqlB[i])
        if datab is not None:
            print('目标端SQL连接测试：成功')
        else:
            ex.append(1)
        print('第%d组SQL连接测试：结束' % (i + 1))
    if len(ex) != 0:
        sys.exit()
    else:
        pass


def testa():
    sqlA = Aconfig()[0]
    sqla = sqlA[0]
    #sqla = "select _date, fund, 净值 from fund_state t where t._date between'20170101'and'20170130'"
    dataa = getdataA(sqla)  #第一条sql语句的返回数据
    print('数据行数：',len(dataa))
    dataa1 = dataa[0]
    print(dataa1)
    for i in range(len(dataa1)):
        if i ==11:
            print(str(dataa1[i]))
        print('第%d个元素类型：'%i,dataa1[i],type(dataa1[i]))

    #print(dataa1[1].decode('utf8'))

def testb():
    sqlB = Bconfig()[0]
    sqlb = sqlB[0]
    #sqlb = "select t.fundcode, t.fundname, t.fullname, t.operstartdate, t.contractenddate, t.primtrustee from fund t"
    #sqlb = "select busidate, fundcode, t.unitnav, t.nav from if_fundassetval t where t.busidate between 20170101 and 20170130 order by fundcode, busidate"
    datab = getdataB(sqlb)
    print('数据行数：',len(datab))
    datab1 = datab[0]
    print(datab1)
    for i in range(len(datab1)):
        print('第%d个元素,类型：'%i,datab1[i],type(datab1[i]))

if __name__ == '__main__':
    testa()
    testb()
    #test()













