import pymysql
import os

# 连接数据库
db = pymysql.connect(host='localhost',
                         user='root',
                         password='@qwer2580',
                         database='SCENERY')
 # 创建访问对象
cursor = db.cursor()  # 也就是游标

folder_path = './hotel/to/folder'  # 文件夹路径

# 获取文件夹中的所有文件名
filenames = []
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        filenames.append(filename)

print(filenames)