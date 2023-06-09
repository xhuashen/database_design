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

# 向数据库中插入数据，给定参数表名，插入的元组,三属性的插入
def insert_user_data(table,account,password,name):
    db = get_db()
    cursor = db.cursor()
    sql="insert into %s values ('%s','%s','%s')" % \
        (table,account,password,name)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()

# 两属性表的插入
def insert_user_data_two(table,account,SYcode):
    db = get_db()
    cursor = db.cursor()
    sql="insert into %s values ('%s','%s')" % \
        (table,account,SYcode)
    print(sql)
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()

def insert_scenery_data(SYcode,SYname,SYinformation,SYTD):
    db = get_db()
    cursor = db.cursor()
    sql="insert into scenery values ('%s','%s','%s','%s',0)" % (SYcode,SYname,SYinformation,SYTD)
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
    scenery_Llke = get_data_by_one_index('SYliked', 'scenery', 'SYcode', city + '%')  # 获得每个城区所有景点的点赞数.3
        # print(scenery_code)
    for i in range(len(scenery_name)):
            # print(i)
        image_path = get_data_by_one_index('Image_path', 'Image', 'SYcode', scenery_code[i][0])[0][0]  # 获得每个景点的第一张图片
        my_dict = {'area_name':area_name,'name':scenery_name[i][0],'description':scenery_describution[i][0],'image':image_path,'like_count':scenery_Llke[i][0]}
        scenery.append(my_dict)
    # print(scenery)
    return scenery

# 将景点名称为spot_name的景点的点赞数＋1
def likeadd(spot_name):
    db = get_db()
    cursor = db.cursor()
    sql = "update scenery set SYliked=SYliked+1 where SYname='%s' " % spot_name
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()


# 存储每个景点的详细信息,以字典的形式，包括spot.name, spot.description spot.location spot.avg_cost , spot.call, spot.image_url1,2,3,用于渲染模板
def get_scenery_detail_list(scenery_name):
    scenery_describution = get_data_by_one_index('SYinformation', 'scenery', 'SYname', scenery_name )[0][0]  # 获得每个景点所有景点的介绍文件路径。3
    scenery_code=get_data_by_one_index('SYcode', 'scenery', 'SYname', scenery_name )[0][0] # 获取景点编号
    image=get_data_by_one_index('Image_path', 'Image', 'SYcode', scenery_code) # 得到三个路径，对于于三张图片
    scenery_describution='C:/Users/19805128155/Desktop/database_design/database_design/scenery/'+scenery_describution
    # 对这个txt文件里面的内容进行解析
    # 定义一个字典来储存这些信息
    with open(scenery_describution, 'r',encoding='utf-8') as f:
        lines = f.readlines()
    result = [line.strip() for line in lines] # 这个列表储存了每一行的元素
    # print(result)
    spot_detail={'name':scenery_name,'description':result[0],
                 'avg_cost':result[3],'location':result[2],'call':result[1],
                 'image_url1':image[0][0],'image_url2':image[1][0],'image_url3':image[2][0]}
    spot_detail['image_url1']='https://github.com/xhuashen/database_design/blob/main/scenery/'+spot_detail['image_url1']+'?raw=true'
    spot_detail['image_url2'] = 'https://github.com/xhuashen/database_design/blob/main/scenery/' + spot_detail['image_url2'] + '?raw=true'
    spot_detail['image_url3'] = 'https://github.com/xhuashen/database_design/blob/main/scenery/' + spot_detail['image_url3'] + '?raw=true'
    return spot_detail


# 要获取，酒店区域hotel_area_name，酒店位置location，酒店名称name，酒店图片image，电话号码call，等级grade
def get_hotel_information(hotel_area_name):
    hotel = []
    hotel_name=[]
    hotel_code=[]
    city=hotel_area_name
    hotel_describution = get_data_by_one_index('hotelinformation', 'hotel', 'hotelcode', city + '%')  # 获得每个城区所有酒店的介绍文件路径
   # print(hotel_describution)
    for i in range(len(hotel_describution)):
        hotel_name.append(hotel_describution[i][0].split("_")[1].split(".")[0])
        hotel_code.append(hotel_describution[i][0].split("_")[0])
    #print(hotel_name)
    #print(hotel_code)
    for i in range(len(hotel_code)):
        # 解析酒店的描述文件
        with open('C:/Users/19805128155/Desktop/database_design/database_design/hotel/hotel_introduction/'+hotel_describution[i][0], 'r', encoding='utf-8') as f:
            lines = f.readlines()
        result = [line.strip().split("+")[1] for line in lines]
        image=get_data_by_one_index('Image', 'hotel_Image', 'image_code', hotel_code[i])[1][0]
        dict={
            'image':'https://github.com/xhuashen/database_design/blob/main/hotel/hotel_image/'+image+'?raw=true',
            'name':hotel_name[i],
            'location':result[2],
            'call':result[3],
            'grade':result[5],
        }
        hotel.append(dict)
        #print(image)
        #print(result)
    #print(hotel)
    return hotel

def get_hotel_detail_list(hotel_name):
    hotel_description=get_data_by_one_index('hotelinformation', 'hotel', 'hotelinformation', '%'+hotel_name + '%')[0][0]
    hotel_code=hotel_description.split("_")[0]
    #print(hotel_description)
    with open('C:/Users/19805128155/Desktop/database_design/database_design/hotel/hotel_introduction/' +hotel_description, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    result = [line.strip().split("+")[1] for line in lines]
    image = get_data_by_one_index('Image', 'hotel_Image', 'image_code', hotel_code)
    dict = {
        'description':result[1],
        'name': hotel_name,
        'location': result[2],
        'call': result[3],
        'url':result[4],
        'image0':'https://github.com/xhuashen/database_design/blob/main/hotel/hotel_image/'+image[0][0]+'?raw=true',
        'image1': 'https://github.com/xhuashen/database_design/blob/main/hotel/hotel_image/' + image[1][0] + '?raw=true',
        'image2': 'https://github.com/xhuashen/database_design/blob/main/hotel/hotel_image/' + image[2][0] + '?raw=true',
        'image3': 'https://github.com/xhuashen/database_design/blob/main/hotel/hotel_image/' + image[3][0] + '?raw=true'

    }
    #print(dict)
    return dict

# 这个函数获取下一个景点或者酒店的主码，也就是编号
def get_next_spot_code(area_name):
    code=get_data_by_one_index('SYcode','scenery','SYcode',area_name+'%')
    return code[-1][0].split("00")[0]+'00'+'%s'% (int(code[-1][0].split("00")[1])+1)

def get_next_hotel_code(area_name):
    code=get_data_by_one_index('hotelcode','hotel','hotelcode',area_name+'%')
    return code[-1][0].split("0")[0]+'0'+'%s'% (int(code[-1][0].split("0")[1])+1)

if  __name__ == '__main__':
    # get_hotel_detail_list('WeiYeNaH')
    print(get_next_hotel_code('PK'))
    print(get_next_spot_code('PK'))
