from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Lock
from serial_reader import ser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import api
import os
 
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomprecision'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

user_logged = {
        'user_uid': '',
        'user_name': '',
        'user_query': '',
        }


db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/conn')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

def background_thread():
    while True:
        socketio.sleep(1)

        uid_read = str(ser.readline().decode('utf-8'))[1:12]

        user_stored = User.query.filter_by(uid=uid_read).first()

        if user_stored is None:
            print('This user is not registered.')
        else:
            user_logged['user_uid'] = user_stored.uid
            user_logged['user_name'] = user_stored.username

       # if user_read != logged_user['user_uid']:
       #     query_result = api.request_tweets()
       #     logged_user['user_result'] = query_result
        #    logged_user['user_uid'] = user_read
         #   logged_user['log_status'] = True
            socketio.emit('server_response', {'data': user_logged}, namespace='/conn')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    resources = db.Column(db.Integer)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == '__main__':
    socketio.run(app, debug=True)
