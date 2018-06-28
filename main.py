from flask import Flask, render_template, request, jsonify
import flask
import boto3
import flask_login

# s3 = boto3.client('s3', aws_access_key_id='',
#     aws_secret_access_key='')

app = Flask(__name__)
app.secret_key = 'abc-abc'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}


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
    return 'Logged in as: ' + flask_login.current_user.id 
    #render_template('ecom.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out' 


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