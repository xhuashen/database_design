import pymysql
import os

# 连接数据库
db = pymysql.connect(host='localhost',
                         user='root',
                         password='@qwer2580',
                         database='SCENERY')
 # 创建访问对象
cursor = db.cursor()  # 也就是游标
folder_path = './hotel_introduction'  # 文件夹路径

# 获取文件夹中的所有文件名
hotel_code=[]
hotel_intro=[]
hotel_image=[]
image_code=[]
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        hotel_intro.append(filename)
# print(hotel_intro)  # 这个为酒店介绍文件
for i in range(len(hotel_intro)):
    hotel_code.append(hotel_intro[i].split("_")[0])
print(hotel_code) # filename 为酒店编号列表
print(hotel_intro)

folder_path = './hotel_image'
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        hotel_image.append(filename)
# print(hotel_image)


for i in range(len(hotel_image)):
    image_code.append(hotel_image[i].split("_")[0])
print(image_code)
print(hotel_image)
for i in range(len(hotel_intro)):
    sql="insert into hotel value('%s','%s')"%(hotel_code[i],hotel_intro[i])
    print(sql)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
for i in range(len(image_code)):
    sql="insert into hotel_image value('%s','%s')" % (image_code[i],hotel_image[i])
    print(sql)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()