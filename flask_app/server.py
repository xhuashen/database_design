from flask import Flask, request, render_template
# import config
import sql
app = Flask(__name__)


# 获取，验证用户登录，登入成功进入首页，否则提示错误
@app.route('/login_request/',methods=['POST'])
def login_request():
    account=request.form.get('username')
    password=request.form.get('password')
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

if  __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)
