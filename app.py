from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
from threading import Lock
from serial_reader import ser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import RPi.GPIO as GPIO
import printer
import sound
import time
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
        'user_choice': '',
        'user_resources': None,
        'user_status': False
        }

# button_counter = 0

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO pins for buttons
# GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.setup(14, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def request_text(channel):
    # print(user_logged['user_name'])
#     data = api.request_quotes()
#     print(data)
#     print('Button Pressed')
#     GPIO.output(14, GPIO.HIGH)
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 1:
        text_requested = api.request_tweets()
        printer.print_tweets()
        print(text_requested)
        current_user.resources -= 1
        db.session.commit()
        print('You spend 1 point.')
        user_logged['user_resources'] = current_user.resources
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
    else:
        print('You cannot afford a text message.')
#     else:
#         print("You can't afford a text message!")

def request_image(channel):
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 2:
        # printer.print_tweets()
        print("You spent 2 points for an image!")
        current_user.resources -= 2
        db.session.commit()
    else:
        print('You cannot afford an image message.')

def request_sound(channel):
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 3:
        # printer.print_tweets()
        print("You spent 3 points for a sound message!")
        sound.play_random_sound()
        current_user.resources -= 3
        db.session.commit()
    else:
        print('You cannot afford a sound message.')

def request_video():
    pass


GPIO.add_event_detect(18, GPIO.FALLING, callback=request_text)
GPIO.add_event_detect(23, GPIO.FALLING, callback=request_image)
GPIO.add_event_detect(16, GPIO.FALLING, callback=request_sound)
# GPIO.add_event_detect(25, GPIO.FALLING, callback=request_video)

# Check the resources the logged user have
# If the remainder is more than required, trigger api query
# def check_resources(user, requirement):
#     if user.user_resource < requirement:
#         return False
#     else:
#         return True

# def listen_button_event():
#
#     if button_state['text_button'] == False:
#         global button_counter
#         button_counter += 1


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
        db.session.commit()
        socketio.sleep(1)
        # 1. first listen for RFID read from user, do user checks etc.
        uid_read = str(ser.readline().decode('utf-8'))[1:12]
        # if uid_read != user_logged['user_uid']:
        stored_user = User.query.filter_by(uid=uid_read).first()
        if stored_user is None:
            pass
        else:
            user_logged['user_uid'] = stored_user.uid
            user_logged['user_name'] = stored_user.username
            user_logged['user_resources'] = stored_user.resources

        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        print(user_logged['user_name'])

    #     uid_read = str(ser.readline().decode('utf-8'))[1:12]
    #     # user_stored = User.query.filter_by(uid=uid_read).first()
    #     if(logIn(uid_read)):
    #         socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
    #     else:
    #         print('log in failed')
    #
    # while user_logged['user_status'] == True:
    #     socketio.sleep(1)
    #     print('Please Press Button')
    #     check_user = User.query.filter_by(uid=user_logged['user_uid']).first()
    #     print(check_user.resources)
    #     socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        # if user_stored is None:
        #     print('This user is not registered.')
        #     print('none')
        # elif user_stored.uid == user_logged['user_uid']:
        #     print('same')
        # else:
        #     print('not same')
        #     user_logged['user_uid'] = user_stored.uid
        #     user_logged['user_name'] = user_stored.username
        #     user_logged['user_resources'] = user_stored.resources
        #     socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
# def logIn(uid_read):
#     # check RFID + check if the user exists in the system
#     user_stored = User.query.filter_by(uid=uid_read).first()
#
#     if len(uid_read) >= 0:
#         if user_stored is None:
#             print('This user is not registered.')
#             return False
#         else:
#             user_logged['user_uid'] = user_stored.uid
#             user_logged['user_name'] = user_stored.username
#             user_logged['user_resources'] = user_stored.resources
#             user_logged['user_status'] = True
#             print(user_logged)
#             return True

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
