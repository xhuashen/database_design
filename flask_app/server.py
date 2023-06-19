from flask import Flask, request, render_template, send_file, jsonify, session, url_for
from werkzeug.utils import redirect
from datetime import datetime
# import config
import sql
app = Flask(__name__)
USER_ACCOUNT=''  # 定义一个全局变量，表示用户
# 获取，验证用户登录，登入成功进入首页，否则提示错误
@app.route('/login_request/',methods=['POST'])
def login_request():
    account=request.form.get('username')
    password=request.form.get('password')
    global USER_ACCOUNT
    USER_ACCOUNT = account
    print(type(USER_ACCOUNT))
    if len(sql.user_login(account,password)):
        return render_template('home.html')
    else:
        return render_template('404.html')


# get 请求获得注册页面
@app.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')


# 实现注册功能
@app.route('/register_request/',methods=['POST'])
def register_request():
    # 获取注册信息
    account=request.form.get('account')
    password=request.form.get('password')
    username=request.form.get('username')
    print(account)
    # 将注册信息导入数据库
    sql.insert_user_data('user',account,password,username)
    print("是否完成这一步")
    # 注册成功后返回登录页面
    return render_template('login.html')

@app.route('/',methods=['GET'])
@app.route('/login/',methods=['GET'])
def login():
    return render_template('login.html')

# 得到地图区域页面
@app.route('/area',methods=['GET'])
def area():
    return render_template('area.html')


@app.route('/hotel_area',methods=['GET'])
def hotel_area():
    return render_template('hotel_area.html')

# 使用动态url传参，获取不同城区的前端页面
@app.route('/area/<area_name>/',methods=["GET"])
def scenery_list(area_name):
    # http: // 114.214 .240.215: 7000 / area = LS
    # print(area_name)
    scenery = sql.get_scenery_list(area_name) # 创建字典列表
    # spots = [
    #     {'id': 1, 'name': '景点1', 'description': '这是一段景点1的简要介绍', 'image': '/static/images/spot1.jpg'},
    #     {'id': 2, 'name': '景点2', 'description': '这是一段景点2的简要介绍', 'image': '/static/images/spot2.jpg'},
    #     {'id': 3, 'name': '景点3', 'description': '这是一段景点3的简要介绍', 'image': '/static/images/spot3.jpg'},
    # ]
    # 从数据库中提取数据
    # 用字典列表存储信息
    # 图片地址：https://github.com/xhuashen/database_design/blob/main/scenery/image/GC00101.jpg
    for i in scenery:
        i['description']='C:/Users/19805128155/Desktop/database_design/database_design/scenery/'+i['description']
        i['image']='https://github.com/xhuashen/database_design/blob/main/scenery/'+i['image']+'?raw=true'
        # print(i['image'])
        with open(i['description'], 'r') as file:
            # 读取文件内容并存储为字符串
            file_contents = file.read()
            i['description']=file_contents
        # 输出文件内容
        # print(i['description'])
    return render_template('scenery.html',title='景点介绍列表',spots=scenery)


@app.route('/hotel_area/<area_name>/',methods=["GET"])
def hotel_list(area_name):
    hotel=sql.get_hotel_information(area_name)
    return render_template('hotel.html',title='酒店介绍列表',hotels=hotel)
# https://github.com/xhuashen/database_design/blob/main/scenery/image/JN00201.jpg?raw=true
# 用户点赞后为用户的收藏表增加一个收藏
@app.route('/api/like', methods=['POST'])
def like():
    spot_id = request.json.get('id')
    print(spot_id)
    sql.likeadd(spot_id)  # 将点击返回到后台，即用户收藏景点，则景点的SYliked属性＋1
    # 将收藏加入用户的收藏列表 # user_account,SYcode,获取SYcode
    sycode=sql.get_data_by_one_index('sycode','scenery','syname',spot_id)[0][0]
    print(sycode)
    print(USER_ACCOUNT)
    sql.insert_user_data_two('user_liked',USER_ACCOUNT,sycode)
    print(USER_ACCOUNT)
    # like_counts=sql.get_data_by_one_index('SYliked','scenery','SYname',spot_id)[0]
    # print(like_counts)
    return


SCENERY=''
# http://114.214.240.215:7000/details/QX+%E6%A0%96%E9%9C%9E%E5%B1%B1
@app.route('/details/<scenery_name>/',methods=["GET"])
def scenery_detail(scenery_name):
    # print(scenery_name) # 这个为QX+栖霞山，将栖霞山给解析出来
    scenery_name = scenery_name.split("+")[1]
    global SCENERY
    SCENERY=scenery_name # 将景点名赋值给全局变量
    # print(scenery_name) # 解析结果
    spot=sql.get_scenery_detail_list(scenery_name)
    # 提取出数据库中的评论信息
    COM=[] # 评论信息的字典列表
    comment=sql.get_data_by_one_index('*','comment','scenery',scenery_name)
    for i in range(len(comment)):
        dict={'username':comment[i][1],'timestamp':TIME,'content':comment[i][2]}
        COM.append(dict)
    return render_template('detail_scenery.html',spot=spot,comments=COM) # comment 参数应该是一个字典列表


@app.route('/hotel_details/<hotel_name>/',methods=["GET"])
def hotel_detail(hotel_name):
    hotel_name=hotel_name.split("+")[1]
    # print(hotel_name) 得到酒店名字
    hotel=sql.get_hotel_detail_list(hotel_name)
    return render_template('hotelintro.html',hotel=hotel)


TIME=''

@app.route('/commet_submit/', methods=['POST'])  # 点击提交之后要进入一个url
def commet_submit():
    # username = request.form.get('username') # 获取景点的用户评论信息
    comment = request.form.get('comment')
    # print(username)
    # print(comment)
    sql.insert_user_data('comment',SCENERY,USER_ACCOUNT,comment)
    now = datetime.now()
    global TIME
    TIME=now # 获取评论时间,评论时间应该放进数据库里面
    # scenery= SCENERY
    # 将评论信息插入
    # 这里需要返回原页面
    # 从会话中获取之前的 URL
    return render_template('submit_success.html')
# @app.route('/route_detail?route_id=1/', methods=['GET'])
# def route_detail1():


if  __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
