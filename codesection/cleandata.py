from codesection.sqlconfig import Aconfig,Bconfig
from codesection.connect import getdataA,getdataB,source,target
import datetime,decimal
import gc,sys

'''
sqlserver数据类型：datetime.datetime decimal.Decimal NoneType        --使用存储过程
oracle对应数据类型：int str NoneType
需要对sqlserver的数据类型进行改变
'''


#对str类型进行编码更改，sqlserver有中文输出问题
def getCode(strText):
    b = bytes((ord(i) for i in strText))
    c = b.decode('gb2312')
    return c

#判断是否是数值型数据
def isFloat(value):
    try:
        float(value)
        return True
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception:
        return False

#对3种数值型str进行处理('0100'不变,'100.00'四舍五入,'100'保留)
def str_number(value):
    if value[0] == '0' or '.' not in value:
        pass
    else:
        value = float(value)
        value = round(value, 9)
        value = str(value)
    return value


############################sqlserver####################################
#sqlserver获得干净数据key：data(数据库返回数据),order(对比参数)
def keya(data, order):
    k = []                                          #主键存放器
    if order[1] == "True":                          #主键是联合主键
        for i in range(len(data)):  # 要遍历的行数
            knum = order[0].split(',')                  # 主键的顺序列表
            vi = []                                     # 主键的多个值存放列表
            if order[2] == '0':                         #没有时间主键
                for j in range(len(knum)):              #遍历主键单个值进行清洗
                    v = data[i][int(knum[j])-1]         #主键的一个值
                    if type(v) == datetime.datetime:    #洗数据
                        v = str(v)
                    elif type(v) == int:
                        v = str(v)
                    elif type(v) == float:
                        v = round(v, 9)
                        v = str(v)
                    elif type(v) == decimal.Decimal:
                        v = float(v)
                        v = round(v, 9)
                        v = str(v)
                    elif v is None:
                        v = str(v)
                    elif type(v) == str:
                        v = getCode(v)
                        if isFloat(v):      #判断str是否为数值型数据
                            v = str_number(v)
                        else:
                            pass
                    else:
                        pass
                    vi.append(v)                        #将主键单个值V添加进vi集合
                vi = '-'.join(vi)                        #组合主键
                k.append(vi)                            #将组合主键添加进存放器
            else:                                       #含有时间主键
                k1 = order[2].split(',')                            # 时间主键的序列值集合k1
                k1iter = iter(k1)                          #knum为非时间主键的序列集合

                for z in range(len(k1)):                        #时间主键的值
                    knum.remove(next(k1iter))
                    v1 = data[i][int(k1[z])-1]
                    if type(v1) == datetime.datetime:           # v1洗数据
                        if v1.month > 9 and v1.day > 9:
                            v1 = str(v1.year) + str(v1.month) + str(v1.day)
                        elif v1.month < 10 and v1.day > 9:
                            v1 = str(v1.year) + '0' + str(v1.month) + str(v1.day)
                        elif v.month > 9 and v.day < 10:
                            v1 = str(v1.year) + str(v1.month) + '0' + str(v1.day)
                        else:
                            v1 = str(v1.year) + '0' + str(v1.month) + '0' + str(v1.day)
                    elif type(v1) == str:
                        v1 = v1[0:8]
                    elif type(v1) == int:
                        v1 = str(v1)[0:8]
                    else:
                        pass
                    vi.append(v1)

                for j in range(len(knum)):                #非时间主键,遍历主键单个值进行清洗
                    v2 = data[i][int(knum[j])-1]            #非时间主键单个值
                    if type(v2) == datetime.datetime:    #洗数据
                        v2 = str(v2)
                    elif type(v2) == int:
                        v2 = str(v2)
                    elif type(v2) == float:
                        v2 = round(v2, 9)
                        v2 = str(v2)
                    elif type(v2) == decimal.Decimal:
                        v2 = float(v2)
                        v2 = round(v2, 9)
                        v2 = str(v2)
                    elif v2 is None:
                        v2 = str(v2)
                    elif type(v2) == str:
                        v2 = getCode(v2)
                        if isFloat(v2):      #判断str是否为数值型数据
                            v2 = str_number(v2)
                        else:
                            pass
                    else:
                        pass
                    vi.append(v2)                       #将主键单个v值添加进vi集合
                vi = '-'.join(vi)                       #组合主键
                k.append(vi)                            # 将组合主键添加进存放器
    else:                                           #主键不是联合主键
        for i in range(len(data)):                  #要遍历的行数
            v = data[i][int(order[0])-1]

            if order[2] != '0':                  #主键是datetime
                if type(v) == datetime.datetime:
                    if v.month > 9 and v.day > 9:
                        v = str(v.year) + str(v.month) + str(v.day)
                    elif v.month < 10 and v.day > 9:
                        v = str(v.year) + '0' + str(v.month) + str(v.day)
                    elif v.month > 9 and v.day < 10:
                        v = str(v.year) + str(v.month) + '0' + str(v.day)
                    else:
                        v = str(v.year) + '0' + str(v.month) + '0' + str(v.day)
                elif type(v) == str:
                    v = v[0:8]
                elif type(v) == int:
                    v = str(v)[0:8]
                else:
                    pass
                k.append(v)
            else :                                  #主键不是datetime
                if type(v) == datetime.datetime:
                    v = str(v)
                elif type(v) == int:
                    v = str(v)
                elif type(v) == float:
                    v = round(v, 9)
                    v = str(v)
                elif type(v) == decimal.Decimal:
                    v = float(v)
                    v = round(v, 9)
                    v = str(v)
                elif v is None:
                    v = str(v)
                elif type(v) == str:
                    v = getCode(v)
                    if isFloat(v):  # 判断str是否为数值型数据
                        v = str_number(v)
                    else:
                        pass
                else:
                    pass
                k.append(v)
    return k

#keys集合接口
def keyas(sql,order):
    data = getdataB(sql)
    k = key(data, order)
    return k

#dataone=data[i]一行数据
def valuea(dataone, order):
    vi = []
    for i in range(len(order[3])):
        v = dataone[int(order[3][i])-1]
        if type(v) == datetime.datetime:
            v = str(v)
            # if v.month > 9 and v.day > 9:
            #     v = str(v.year) + str(v.month) + str(v.day)
            # elif v.month < 10 and v.day > 9:
            #     v = str(v.year) + '0' + str(v.month) + str(v.day)
            # elif v.month > 9 and v.day < 10:
            #     v = str(v.year) + str(v.month) + '0' + str(v.day)
            # else:
            #     v = str(v.year) + '0' + str(v.month) + '0' + str(v.day)
        elif type(v) == int:
            v = str(v)
        elif type(v) == float:
            v = round(v, 9)
            v = str(v)
        elif type(v) == decimal.Decimal:
            v = float(v)
            v = round(v, 9)
            v = str(v)
        elif v is None:
            v = str(v)
        elif type(v) == str:
            v = getCode(v)
            if isFloat(v):  # 判断str是否为数值型数据
                v = str_number(v)
            else:
                pass
        else:
            pass
        vi.append(v)
    return vi


#获得干净数据values：data(数据库返回数据),order(对比参数)
def valueas(data, order):
    vs = []
    for i in range(len(data)):
        dataone = data[i]
        #print(dataone)
        vi = valuea(dataone,order)
        vs.append(vi)
    del data, order
    gc.collect()
    return vs


#############################Oracel####################################
#Oracel获得干净数据key：data(数据库返回数据),order(对比参数)
def key(data, order):
    k = []
    if order[1] == "True":                          #主键是联合主键
        for i in range(len(data)):  # 要遍历的行数
            knum = order[0].split(',')                  # 主键的顺序列表
            vi = []                                     # 主键的多个值存放列表
            if order[2] == '0':                         #没有时间主键
                for j in range(len(knum)):              #遍历主键单个值进行清洗
                    v = data[i][int(knum[j])-1]         #主键的一个值
                    if type(v) == datetime.datetime:    #洗数据
                        v = str(v)
                    elif type(v) == int:
                        v = str(v)
                    elif type(v) == float:
                        v = round(v, 9)
                        v = str(v)
                    elif type(v) == decimal.Decimal:
                        v = float(v)
                        v = round(v, 9)
                        v = str(v)
                    elif v is None:
                        v = str(v)
                    elif type(v) == str:
                        if isFloat(v):  # 判断str是否为数值型数据
                            v = str_number(v)
                        else:
                            pass
                    else:
                        pass
                    vi.append(v)                        #将主键单个值V添加进vi集合
                vi = '-'.join(vi)                        #组合主键
                k.append(vi)                            #将组合主键添加进存放器
            else:                                       #含有时间主键
                k1 = order[2].split(',')                # 时间主键的序列值集合k1
                k1iter = iter(k1)                    # knum为非时间主键的序列集合

                for z in range(len(k1)):                # 时间主键的值
                    knum.remove(next(k1iter))
                    v1 = data[i][int(k1[z]) - 1]
                    if type(v1) == datetime.datetime:   # v1洗数据
                        if v1.month > 9 and v1.day > 9:
                            v1 = str(v1.year) + str(v1.month) + str(v1.day)
                        elif v1.month < 10 and v1.day > 9:
                            v1 = str(v1.year) + '0' + str(v1.month) + str(v1.day)
                        elif v.month > 9 and v.day < 10:
                            v1 = str(v1.year) + str(v1.month) + '0' + str(v1.day)
                        else:
                            v1 = str(v1.year) + '0' + str(v1.month) + '0' + str(v1.day)
                    elif type(v1) == str:
                        v1 = v1[0:8]
                    elif type(v1) == int:
                        v1 = str(v1)[0:8]
                    else:
                        pass
                    vi.append(v1)

                for j in range(len(knum)):                #非时间主键,遍历主键单个值进行清洗
                    v2 = data[i][int(knum[j])-1]            #非时间主键单个值
                    if type(v2) == datetime.datetime:    #洗数据
                        v2 = str(v2)
                    elif type(v2) == int:
                        v2 = str(v2)
                    elif type(v2) == float:
                        v2 = round(v2, 9)
                        v2 = str(v2)
                    elif type(v2) == decimal.Decimal:
                        v2 = float(v2)
                        v2 = round(v2, 9)
                        v2 = str(v2)
                    elif v2 is None:
                        v2 = str(v2)
                    elif type(v2) == str:
                        if isFloat(v2):  # 判断str是否为数值型数据
                            v2 = str_number(v2)
                        else:
                            pass
                    else:
                        pass
                    vi.append(v2)                       #将主键单个v值添加进vi集合
                vi = '-'.join(vi)                       #组合主键
                k.append(vi)                            # 将组合主键添加进存放器
    else:                                           #主键不是联合主键
        for i in range(len(data)):                  #要遍历的行数
            v = data[i][int(order[0])-1]

            if order[2] != '0':                  #主键是datetime
                if type(v) == datetime.datetime:
                    if v.month > 9 and v.day > 9:
                        v = str(v.year) + str(v.month) + str(v.day)
                    elif v.month < 10 and v.day > 9:
                        v = str(v.year) + '0' + str(v.month) + str(v.day)
                    elif v.month > 9 and v.day < 10:
                        v = str(v.year) + str(v.month) + '0' + str(v.day)
                    else:
                        v = str(v.year) + '0' + str(v.month) + '0' + str(v.day)
                elif type(v) == str:
                    v = v[0:8]
                elif type(v) == int:
                    v = str(v)[0:8]
                else:
                    pass
                k.append(v)
            else :                                  #主键不是datetime
                if type(v) == datetime.datetime:
                    v = str(v)
                elif type(v) == int:
                    v = str(v)
                elif type(v) == float:
                    v = round(v, 9)
                    v = str(v)
                elif type(v) == decimal.Decimal:
                    v = float(v)
                    v = round(v, 9)
                    v = str(v)
                elif v is None:
                    v = str(v)
                elif type(v) == str:
                    if isFloat(v):  # 判断str是否为数值型数据
                        v = str_number(v)
                    else:
                        pass
                else:
                    pass
                k.append(v)
    del data
    gc.collect()
    return k

def value(dataone, order):
    vi = []
    for i in range(len(order[3])):
        v = dataone[int(order[3][i])-1]
        if type(v) == datetime.datetime:
            v = str(v)
            # if v.month > 9 and v.day > 9:
            #     v = str(v.year) + str(v.month) + str(v.day)
            # elif v.month < 10 and v.day > 9:
            #     v = str(v.year) + '0' + str(v.month) + str(v.day)
            # elif v.month > 9 and v.day < 10:
            #     v = str(v.year) + str(v.month) + '0' + str(v.day)
            # else:
            #     v = str(v.year) + '0' + str(v.month) + '0' + str(v.day)
        elif type(v) == int:
            v = str(v)
        elif type(v) == float:
            v = round(v, 9)
            v = str(v)
        elif type(v) == decimal.Decimal:
            v = float(v)
            v = round(v, 9)
            v = str(v)
        elif v is None:
            v = str(v)
        elif type(v) == str:
            if isFloat(v):  # 判断str是否为数值型数据
                v = str_number(v)
            else:
                pass
        else:
            pass
        vi.append(v)
    return vi


#获得干净数据values：data(数据库返回数据),order(对比参数)
def values(data, order):
    vs = []
    for i in range(len(data)):
        dataone = data[i]
        #print(dataone)
        vi = value(dataone,order)
        vs.append(vi)
    del data,order
    gc.collect()
    return vs

##############################END####################################

#keysA
#keysB


#获得干净的比对数据A字典类型：sql(单条sql语句),order(对应的比对参数)
#{'20170103': ['10', '主题', '20170103', '602890.4200', '1205177.45', '1107829.9300', '2209370.75', '0.0000', '0.00', '0.00', '0.0000'],...}
def clean_dataA(sql,order):
    sou = source()
    data = getdataA(sql)
    if sou == 'SQLSERVER':
        k = keya(data, order)
        vs = valueas(data, order)
        cleandt = {}
        for i in range(len(k)):
            ki = str(k[i])
            if ki in cleandt.keys():
                print('ERROR:源端数据库A配置的主键不具备唯一性，请修改哈...')
                print('提示一下：第%d行，主键：%s 覆盖了前面的主键'%(i+1, ki))
                sys.exit()
            else:
                cleandt[str(k[i])] = vs[i]
        print("A源端数据清洗：成功")
        del data, k, order, sql, vs
        gc.collect()
        return cleandt
    elif sou == 'ORACLE':
        k = key(data, order)
        vs = values(data, order)
        cleandt = {}
        for i in range(len(k)):
            ki = str(k[i])
            if ki in cleandt.keys():
                print('ERROR:源端数据库A配置的主键不具备唯一性，请修改哈...')
                print('提示一下：第%d行，主键%s 覆盖了前面的主键'%(i+1, ki))
                sys.exit()
            else:
                cleandt[str(k[i])] = vs[i]
        print("A源端数据清洗：成功")
        del data,k,order,sql,vs
        gc.collect()
        return cleandt


#获得干净的比对数据B字典类型：sql(单条sql语句),order(对应的比对参数)
def clean_dataB(sql,order):
    tar = target()
    data = getdataB(sql)
    if tar == 'SQLSERVER':
        k = keya(data, order)
        vs = valueas(data, order)
        cleandt = {}
        for i in range(len(k)):
            ki = str(k[i])
            if ki in cleandt.keys():
                print('ERROR:比对数据库配B置的主键不具备唯一性，请修改哈...')
                print('提示一下：第%d行，主键%s 覆盖了前面的主键'%(i+1, ki))
                sys.exit()
            else:
                cleandt[str(k[i])] = vs[i]
        print("B比对端数据清洗：成功")
        del tar, data, k,
        gc.collect()
        return cleandt
    elif tar == 'ORACLE':
        k = key(data, order)
        vs = values(data, order)
        cleandt = {}
        for i in range(len(k)):
            ki = str(k[i])
            if ki in cleandt.keys():
                print('ERROR:比对数据库B配置的主键不具备唯一性，请修改哈...')
                print('提示一下：第%d行，主键%s 覆盖了前面的主键'%(i+1, ki))
                sys.exit()
            else:
                cleandt[str(k[i])] = vs[i]
        print("B比对数据清洗：成功")
        del tar,data,k,
        gc.collect()
        return cleandt

#测试代码
def testa():
    sqlA = Aconfig()[0]
    sql = sqlA[0]
    orderA = Aconfig()[1]
    order = orderA[0]
    cleandtA = clean_dataA(sql, order)
    print(cleandtA["059003-工行积极配置"])
    print(type(cleandtA["059003-工行积极配置"][7]))
    print(1,cleandtA["059003-工行积极配置"][7])
def testb():
    sqlB = Bconfig()[0]
    sql = sqlB[0]
    orderB = Bconfig()[1]
    order = orderB[0]
    cleandtB = clean_dataB(sql, order)
    print(cleandtB["059003-工行积极配置"])
    print(type(cleandtB["059003-工行积极配置"][7]))
    print(1, cleandtB["059003-工行积极配置"][7])

if __name__ == '__main__':
    testa()
    testb()