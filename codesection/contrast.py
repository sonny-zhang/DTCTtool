from codesection.sqlconfig import Aconfig,Bconfig
from codesection.connect import source,target
from codesection.cleandata import clean_dataA,clean_dataB
from xlutils.copy import copy
import xlwt,xlrd
import os, time, math, gc

sqlsA  = Aconfig()[0]   #Asql语句的的集合
sqlsB  = Bconfig()[0]   #Bsql语句的集合

#获取A的单条sql语句，order
def sqlA(i):
    sql = sqlsA[i]
    orderA = Aconfig()[1]
    order = orderA[i]
    return sql,order

#获取B的单条sql语句集合，order
def sqlB(i):
    sql = sqlsB[i]
    orderB = Bconfig()[1]
    order = orderB[i]
    return sql,order

#B有主键key，A没有该主键key的集合keysB
def unkeyA(i):
    dataB = clean_dataB(sqlB(i)[0], sqlB(i)[1])
    dataA = clean_dataA(sqlA(i)[0], sqlA(i)[1])
    keyBiter = iter(dataB.keys())
    keysB = []
    for j in range(len(dataB.keys())):
        keyB = next(keyBiter)
        if keyB not in dataA.keys():
            keysB.append(keyB)
        else:
            pass
    del dataB,dataA
    gc.collect()
    return keysB

#Excel写入样式设置
def set_style(name,height,color,bold=False):
    style = xlwt.XFStyle()      #初始化样式

    font = xlwt.Font()          #为样式创建字体
    font.name = name            #字体类型
    font.colour_index = 8   #字体颜色
    font.height = height        #字体大小
    style.font = font           #定义格式

    # 设置背景颜色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN    #设置背景颜色的模式
    pattern.pattern_fore_colour = color     #背景颜色
    style.pattern = pattern     #定义格式
    return style

#创建空sheet
def create_excel(i):
    f = xlwt.Workbook()         #创建excel文件
    #创建sheet，并指定可以重复写入数据的情况，设置行高

    dataA = clean_dataA(sqlA(i)[0], sqlA(i)[1])
    nums = len(dataA.keys())
    nums1 = len(unkeyA(i))
    num1 = math.ceil( nums1 / 65000 )
    num = math.ceil(nums / 65000)
    num = num + num1
    for k in range(num):
        f.add_sheet('sheet%d'%(k+1), cell_overwrite_ok=False)

    ff = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    nowt = time.strftime('%Y-%m-%d#%H%M%S', time.localtime())
    fff = os.path.join(ff, 'results', 'result%d(%s).xls'%(i+1,nowt))
    file = fff.replace('\\', '/')
    # print(file)
    f.save(file)# 保存文档
    del dataA
    gc.collect()
    FILE = file
    print('result%d.xls创建成功,开始写入...'%(i+1))
    return FILE        #FILE是要写入的文件路径名,num是Excel的sheet数量

#判断字符串是否是数值(int，float)
def isFloat(value):
    try:
        x = float(value)
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception as e:
        return False
    else:
        return True

#填写sheet：
def write_excel(i):

    # ff = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    # fff = os.path.join(ff, 'results', 'results.xls')
    # file = fff.replace('\\', '/')
    file = create_excel(i)

    oldwb = xlrd.open_workbook(file,formatting_info=True)
    newwb = copy(oldwb)

    r = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    rr = os.path.join(r, 'config', 'sqlconfig.xls')
    rfile = rr.replace('\\', '/')
    workbook = xlrd.open_workbook(rfile, formatting_info=True, encoding_override='utf-8')
    sheet1 = workbook.sheet_by_index(0)
    row0 = sheet1.row_values(0)[0:8]
    row1 = sheet1.row_values(2 * i + 1)[0:8]
    row2 = sheet1.row_values(2 * (i + 1))[0:7]
    if len(row1[7]) == 1:               #需要对对比顺序的值做下判断，特殊情况：1个值
        row4 = list(row1[7])
    else:
        row4 = row1[7].split(',')
    if len(row1[6]) == 1:               #需要对对比顺序的值做下判断，特殊情况：1个值
        rowA5 = list(row1[6])
    else:
        rowA5 = row1[6].split(',')
    row5 = ['源端数据A', '对比数据B', '差值']
    green = set_style('Times New Roman', 220, 42)
    green1 = set_style('Times New Roman', 220, 50)
    pink = set_style('Times New Roman', 220, 29)
    yellow = set_style('Times New Roman', 220, 51)
    red = set_style('Times New Roman', 220, 2)
    white = set_style('Times New Roman', 220, 82)
    purple = set_style('Times New Roman', 220, 46)

    dataA = clean_dataA(sqlA(i)[0], sqlA(i)[1])
    dataB = clean_dataB(sqlB(i)[0], sqlB(i)[1])

    #分类填写：A有，B有；A有，B无
    keys = iter(dataA.keys())  # A的keys
    nums = len(dataA.keys())
    num = math.ceil(nums / 65000)         #num是以源端数据库的sheet数
    onesheet = nums                       #一个sheet为65000行
    for n in range(num):                  #对要写入的sheet进行遍历并写入sheet
        sheeti = newwb.get_sheet(n)

        print('开始写入sheet%d...'%(n+1))

        # 写入rowi0
        for j in range(len(row0)):
            sheeti.write(0, j, row0[j], green)

        # 写入row1
        for j in range(len(row1)):
            sheeti.write(1, j, row1[j], pink)

        # 写入row2
        for j in range(len(row2)):
            sheeti.write(2, j, row2[j], pink)

        #写入row4
        for j in range(len(row4)):
            sheeti.write(4, j*3+2, row4[j], yellow)

        #写入row5
        sheeti.write(5, 0, '条数', yellow)
        sheeti.write(5, 1, '主键', yellow)

        for j in range(len(rowA5)):
            sheeti.write(5, 3*j+2, row5[0], yellow)
            sheeti.write(5, 3*(j+1), row5[1], yellow)
            sheeti.write(5, 3*(j+1)+1, row5[2], yellow)

        # 写入data
        if onesheet > 65000:
            j = 0
            while j< 65000:                                       #判断写满一个sheet(行数65000)
                key = next(keys)                                    #A的key

                sheeti.write(6+j, 0, j+1, white)

                if key in dataB.keys():                                 # 主键都存在
                    sheeti.write(6 + j, 1, key, white)  # 主键写入
                    for k in range(len(dataA[key])):  # 对values进行遍历
                        A = dataA[key][k]
                        B = dataB[key][k]
                        if A == B:
                            sheeti.write(6 + j, 3 * k + 2, A, white)
                            sheeti.write(6 + j, 3 * (k + 1), B, white)
                        if A != B:
                            if isFloat(A) and isFloat(B):
                                C = float(A) - float(B)
                                sheeti.write(6 + j, 3 * k + 2, A, red)
                                sheeti.write(6 + j, 3 * (k + 1), B, red)
                                sheeti.write(6 + j, 3 * (k + 1) + 1, C, white)
                            else:
                                sheeti.write(6 + j, 3 * k + 2, A, red)
                                sheeti.write(6 + j, 3 * (k + 1), B, red)
                else:                                                   # 主键A存在，B不存在
                    sheeti.write(6 + j, 1, key, purple)  # 主键写入
                    for k in range(len(dataA[key])):  # 对values进行遍历
                        A = dataA[key][k]
                        sheeti.write(6 + j, 3 * k + 2, A, purple)
                        sheeti.write(6 + j, 3 * (k + 1), '', purple)
                        sheeti.write(6 + j, 3 * (k + 1) + 1, '', purple)
                j+=1
            onesheet = onesheet-65000
        else:
            for j in range(onesheet):                                       #遍历写满一个sheet(行数onesheet)
                key = next(keys)            #A的key
                sheeti.write(6+j, 0, j+1, white)

                if key in dataB.keys():                                     # 主键A存在，B存在
                    sheeti.write(6 + j, 1, key, white)

                    for k in range(len(dataA[key])):  # 对values进行遍历
                        A = dataA[key][k]
                        B = dataB[key][k]
                        if A == B:
                            sheeti.write(6 + j, 3 * k + 2, A, white)
                            sheeti.write(6 + j, 3 * (k + 1), B, white)
                        if A != B:
                            if isFloat(A) and isFloat(B):
                                C = float(A) - float(B)
                                sheeti.write(6 + j, 3 * k + 2, A, red)
                                sheeti.write(6 + j, 3 * (k + 1), B, red)
                                sheeti.write(6 + j, 3 * (k + 1) + 1, C, white)
                            else:
                                sheeti.write(6 + j, 3 * k + 2, A, red)
                                sheeti.write(6 + j, 3 * (k + 1), B, red)
                else:                                                           # 主键A存在，B不存在
                    sheeti.write(6 + j, 1, key, purple)  # 主键写入
                    for k in range(len(dataA[key])):  # 对values进行遍历
                        A = dataA[key][k]
                        sheeti.write(6 + j, 3 * k + 2, A, purple)
                        sheeti.write(6 + j, 3 * (k + 1), '', purple)
                        sheeti.write(6 + j, 3 * (k + 1) + 1, '', purple)
                j += 1

        print('结束写入sheet%d...' % (n + 1))

    # 分类填写：B有，A无
    unkA = unkeyA(i)
    if len(unkA) == 0:                          #没有这种情况时：B有，A无
        pass
    else:                                       #有这种情况时：B有，A无
        keysB = iter(unkA)                     #keysB是：A中无B的主键的集合
        numsB = len(unkA)
        numB = math.ceil(numsB / 65000) + num         #numB是所有sheet数
        onesheetB = numsB
        for n in range(num, numB):
            sheeti = newwb.get_sheet(n)

            print('开始写入sheet%d...' % (n + 1))

            # 写入rowi0
            for j in range(len(row0)):
                sheeti.write(0, j, row0[j], green)

            # 写入row1
            for j in range(len(row1)):
                sheeti.write(1, j, row1[j], pink)

            # 写入row2
            for j in range(len(row2)):
                sheeti.write(2, j, row2[j], pink)

            # 写入row4
            for j in range(len(row4)):
                sheeti.write(4, j * 3 + 2, row4[j], yellow)

            # 写入row5
            sheeti.write(5, 0, '条数', yellow)
            sheeti.write(5, 1, '主键', yellow)

            for j in range(len(rowA5)):
                sheeti.write(5, 3 * j + 2, row5[0], yellow)
                sheeti.write(5, 3 * (j + 1), row5[1], yellow)
                sheeti.write(5, 3 * (j + 1) + 1, row5[2], yellow)

            # 写入data
            if onesheetB > 65000:
                j = 0
                while j < 65000:  # 判断写满一个sheet
                    key = next(keysB)  # B的key

                    sheeti.write(6 + j, 0, j + 1, white)
                    sheeti.write(6 + j, 1, key, green1)  # 主键写入
                    for k in range(len(dataB[key])):  # 对values进行遍历
                        B = dataB[key][k]
                        sheeti.write(6 + j, 3 * k + 2, '', green1)
                        sheeti.write(6 + j, 3 * (k + 1), B, green1)
                        sheeti.write(6 + j, 3 * (k + 1) + 1, '', green1)
                    j += 1
                onesheetB = onesheetB - 65000
            else:
                for j in range(onesheetB):  # 判断写满一个sheet
                    key = next(keysB)  # B的key
                    sheeti.write(6 + j, 0, j + 1, white)
                    sheeti.write(6 + j, 1, key, green1)

                    for k in range(len(dataB[key])):  # 对values进行遍历
                        B = dataB[key][k]
                        sheeti.write(6 + j, 3 * k + 2, '', green1)
                        sheeti.write(6 + j, 3 * (k + 1), B, green1)
                        sheeti.write(6 + j, 3 * (k + 1) + 1, '', green1)
            print('结束写入sheet%d...' % (n + 1))

    newwb.save(file)


#从sql语句集里面执行对比函数，Excel写入函数：
def iterator():

    ff = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    fff = os.path.join(ff, 'results', 'results.xls')
    #file = fff.replace('\\', '/')
    #判断是否有results.xls文件
    if os.path.exists(fff):
        print('results.xls文件请先删除')
        return False
    else:
        for i in range(len(sqlsB)):
            write_excel(i)


#测试代码：测试两组sql
def test():
    ff = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    fff = os.path.join(ff, 'results', 'results.xls')
    # file = fff.replace('\\', '/')
    # 判断是否有results.xls文件
    if os.path.exists(fff):
        print('results.xls文件请先删除')
        return False
    else:
        for i in range(len(sqlsB)):
            write_excel(i)

if __name__=='__main__':
    test()
    # print(unkeyA(0))
    # print(len(unkeyA(0)))
