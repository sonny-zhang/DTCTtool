import xlrd
import os

def sqlnum():
    # 打开文件
    f = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))     #上级目录
    ff = os.path.join(f,'config','sqlconfig.xls')
    file = ff.replace('\\','/')
    try:
        workbook = xlrd.open_workbook(file, formatting_info=True, encoding_override='utf-8')
        # 根据sheet索引或者名称获取sheet内容
        sheet1 = workbook.sheet_by_index(0)
        # 获取sql对比次数
        num = len(sheet1.merged_cells)          #用单元格记录几组SQL语句
        return num,sheet1
    except Exception as e:
        print('Error:',e)


#读取SQL语句，对比参数
def read_excel(num, sheet1):
    sqlA = []
    sqlA_order = []
    sqlB = []
    sqlB_order = []
    if num == 0:
        print('Erroe:sqlconfig.xls文件第一列需要合并单元格')
        return False
    else:
        for k in range(num):

            sqlArows = sheet1.row_values(2*k+1)
            #sqlArows[3] = int(sqlArows[3])          #主键序号
            sqlArows[6] = sqlArows[6].split(',')    #对比顺序
            #print(type(sqlArows),sqlArows)
            sqlA.append(sqlArows[2])                #SQL语句
            sqlA_order.append(sqlArows[3:8])        #对比参数集合
            #print(type(sqlA_order),sqlA_order)


            sqlBrows = sheet1.row_values(2*(k+1))
            #sqlBrows[3] = int(sqlBrows[3])
            sqlBrows[6] = sqlBrows[6].split(',')
            sqlB.append(sqlBrows[2])
            sqlB_order.append(sqlBrows[3:8])


        #print(type(sqlB_order))
        return sqlA,sqlA_order,sqlB, sqlB_order

#Asql，order的集合
def Aconfig():
    num = sqlnum()[0]
    sheet1 = sqlnum()[1]
    sqlA = read_excel(num, sheet1)[0]
    sqlA_order = read_excel(num, sheet1)[1]
    # print('sqlA:', sqlA)
    # print(sqlA_order)
    return sqlA, sqlA_order

#Bsql，order的集合
def Bconfig():
    num = sqlnum()[0]
    sheet1 = sqlnum()[1]
    sqlB = read_excel(num, sheet1)[2]
    sqlB_order = read_excel(num, sheet1)[3]
    # print('sqlB:', sqlB)
    # print(sqlB_order)
    return sqlB, sqlB_order


# if __name__ == "__main__":
#     Aconfig()
#     Bconfig()
