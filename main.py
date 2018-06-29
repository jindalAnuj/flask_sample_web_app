from flask import Flask, render_template, request, jsonify
import flask
import boto3
import flask_login
import mysql.connector

# db = mysql.connector.connect(host="anujjindal.cn6fcrgoswsm.ap-south-1.rds.amazonaws.com",
#                     user="anujjindal",password="anuj123.awsdb",db="anujjindal")

app = Flask(__name__)
app.secret_key = 'abc-abc'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'admin@gmail.com': {'password': 'secret'}}


class User(flask_login.UserMixin):
    pass


@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return 

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('ecom.html')
    
    # 'Logged in as: ' + flask_login.current_user.id 
# @app.route('/goback')
# def goback():
#     return render_template('ecom.html')
    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if flask.request.method == 'GET':
        return 
    flask_login.logout_user()
    return 'Logged out' 

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if flask.request.method == 'GET':
        return 
    print('check2')
    product_list = request.form.getlist("prod")
    print(product_list)
    amount = 0
    db = mysql.connector.connect(host="localhost",
                    user="root",password="root",db="test",port="3306")

    cursor = db.cursor()
    for p in product_list:
        print(p)
        if(p =='prod1'):
            amount = amount+20
            cursor.execute("""INSERT INTO test.order (price,name) VALUES (%s,%s)""",('20',p)) 
            print ('check3')
            db.commit()


        if(p =='prod2'):
            amount = amount+30
            cursor.execute("""INSERT INTO test.order(price,
            name)
            VALUES (%s,%s)""",(30,p)) 
            print ('check4')
            db.commit()


        if(p =='prod3'):
            amount = amount+40
            cursor.execute("""INSERT INTO test.order(price,
            name)
            VALUES (%s,%s)""",(40,p)) 
            print ('check5')
            db.commit()
    db.close()
    return render_template('final.html',amt=amount)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized' 
# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/', methods=['POST'])
# def hello():
# 	bucket_name = request.form['text']
# 	file_name = request.form['theFile']
# 	# bucket_name = 'project1s3'
# 	s3.create_bucket(Bucket=bucket_name)
# 	s3.upload_file(file_name, bucket_name, file_name)
# 	print(file_name)
# 	#render_template('gui2.html')
# 	data= []
# 	response = s3.list_buckets()
# 	buckets = [bucket['Name'] for bucket in response['Buckets']]
# 	print("Bucket List: %s" % buckets)
# 	for key in s3.list_objects(Bucket=bucket_name)['Contents']:
# 		data.append(key['Key'])
# 	print(data)
# 	return render_template('gui2.html', name = bucket_name, data = data)

 


if __name__ == '__main__':
    app.run(port = 8080, debug=True)
  # app.run(host = '0.0.0.0' ,port = 8080)