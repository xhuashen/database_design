import pymysql
import os
# 连接数据库
db = pymysql.connect(host='localhost',
                     user='root',
                     password='@qwer2580',
                     database='SCENERY')
# 创建访问对象
cursor = db.cursor()  # 也就是游标
def readtxt(file):  # 读取表格数据为一个二维列表
    class_val = []
    with open(file, encoding='utf8') as fp:
        for line in fp:
            line = line.strip('\n').split()
            class_val.append(line)
    return class_val

# 导入scenery
data = readtxt("./scenery.txt")
for i in range(1,len(data)):
    sql="insert into Scenery values('{}','{}','{}','{}','{}','{}')".format(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],0)
    cursor.execute(sql)
    db.commit()


# 导入scenery_image
data_image=readtxt("./scenery_image.txt")
for i in range(1,len(data_image)):
    sql="insert into Image values('{}','{}')".format(data_image[i][0],data_image[i][1])
    cursor.execute(sql)
    db.commit()

# 关闭数据库连接
db.close()

