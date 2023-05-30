import pymysql
import os

# 读取txt表格的函数
def readtxt(file):  # 读取表格数据为一个二维列表
    class_val = []
    with open(file, encoding='utf8') as fp:
        for line in fp:
            line = line.strip('\n').split()
            class_val.append(line)
    return class_val

def insertdata():
    # 连接数据库
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='@qwer2580',
                         database='SCENERY')
    # 创建访问对象
    cursor = db.cursor()  # 也就是游标

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

    # 导入location
    data_location=readtxt("./loaction.txt")
    for i in range(1,len(data_location)):
        sql = "insert into Location values('{}','{}')".format(data_location[i][0], data_location[i][1])
        cursor.execute(sql)
        db.commit()

    # 导入user
    data_user=readtxt("C:/Users/19805128155/Desktop/database_design/database_design/user/user.txt")
    for i in range(1,len(data_user)):
        sql="insert into user  values('{}','{}')".format(data_user[i][0],data_user[i][1])
        cursor.execute(sql)
        db.commit()
    # 关闭数据库连接
    db.close()

# full folder introduction and distribution
def full_folder():
    data = readtxt("./scenery.txt")
    folder_path_introduction="C:/Users/19805128155/Desktop/database_design/database_design/scenery/scenery_introduction/"
    folder_path_distribution="C:/Users/19805128155/Desktop/database_design/database_design/scenery/Tourist_distribution/"
    for i in range(1, len(data)):
        file_name = data[i][0]+'.txt'
        file_path = os.path.join(folder_path_introduction, file_name)
        with open(file_path, 'w') as f:
            f.write("please write scenery introduction")
        file_paths = os.path.join(folder_path_distribution, file_name)
        with open(file_paths, 'w') as f:
            f.write("please write scenery Tourist distribution")

