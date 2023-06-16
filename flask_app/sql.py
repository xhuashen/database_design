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
    print('comm')



if  __name__ == '__main__':
    user='user'
    insert_user_data(user, 'sakdhas', 'asdas', 'asfas')