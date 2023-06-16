# 这个py文件用了写各种python语句的返回结果
import pymysql

# 连接数据库，返回数据库对象
def get_db():
    try:
        db = pymysql.connect(host="localhost", port=3306, user="root", passwd="@qwer2580", db="SCENERY", charset="utf8")
    except:
        db = None

    return db


# 给定账号密码返回用户名
def user_login(userId, password):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT user_name FROM user WHERE user_account = '%s' && user_password = '%s'" % \
          (userId, password)
    try:
        # 执行sql语句
        cursor.execute(sql)
        name = cursor.fetchall()

        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return name

# 关闭数据库
def db_close():
    db = get_db()
    if db is not None:
        db.close()

# 获取数据库信息，以元组列表的形式返回值
def get_data_from_tabel(tabel):
    db = get_db()
    cursor = db.cursor()
    sql="select * from %s  " % tabel
    cursor.execute(sql)
    data=cursor.fetchall()
    data=list(data)
    return data

# 向数据库中插入数据，给定参数表名，插入的元组
def insert_user_data(table,account,password,name):
    db = get_db()
    cursor = db.cursor()
    sql="insert into %s values ('%s','%s','%s')" % \
        (table,account,password,name)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()

# 单表查询，单条件,查询单属性
def get_data_by_one_index(find_index,table,index,value):
    db = get_db()
    cursor = db.cursor()
    sql="select %s from %s where %s like '%s'" % (find_index,table,index,value)
    cursor.execute(sql)
    data=cursor.fetchall()
    data=list(data)
    return data
def get_scenery_list(area_name): # 这个函数没问题
    scenery=[]
    db = get_db()
    cursor = db.cursor()
    # spots = [
    #     {'id': 1, 'name': '景点1', 'description': '这是一段景点1的简要介绍', 'image': '/static/images/spot1.jpg'},
    #     {'id': 2, 'name': '景点2', 'description': '这是一段景点2的简要介绍', 'image': '/static/images/spot2.jpg'},
    #     {'id': 3, 'name': '景点3', 'description': '这是一段景点3的简要介绍', 'image': '/static/images/spot3.jpg'},
    # ]
    #for location in get_data_from_tabel('location'):
    city=area_name
    scenery_describution = get_data_by_one_index('SYTD','scenery','SYcode',city+'%') # 获得每个城区所有景点的介绍文件路径。3
        # print(scenery_describution)
    scenery_name = get_data_by_one_index('SYname', 'scenery', 'SYcode', city+'%') # 获得每个城区的所有景点的名称，3
        # print(scenery_name)
    scenery_code = get_data_by_one_index('SYcode', 'scenery', 'SYcode', city+'%') # 获得每个城区所有景点的编号.3
        # print(scenery_code)
    for i in range(len(scenery_name)):
            # print(i)
        image_path = get_data_by_one_index('Image_path', 'Image', 'SYcode', scenery_code[i][0])[0][0]  # 获得每个景点的第一张图片
        my_dict = {'area_name':area_name,'name':scenery_name[i][0],'description':scenery_describution[i][0],'image':image_path}
        scenery.append(my_dict)
    print(scenery)
    return scenery


if  __name__ == '__main__':
    # data=get_data_by_one_index('Image_path','Image','SYcode','GC%')
    # print(get_data_from_tabel('location'))
    # print(data)
    # print(get_data_by_one_index('SYname','scenery','SYcode','GC%'))
    #for i in get_scenery_list():
    #    print(i)
    print(get_scenery_list('GC'))