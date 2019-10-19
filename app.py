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
import led
 
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomprecision'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

user_logged = {
        'user_uid': '',
        'user_name': 'No User',
        'user_query': '',
        'user_choice': '',
        'user_resources': None,
        'user_status': False,
        'message': 'What do you want to query from us?'
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
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(2, GPIO.OUT) # setup the blue light
GPIO.setup(3, GPIO.OUT) # setup the red light
GPIO.setup(4, GPIO.OUT) # setup the yellow light
GPIO.setup(5, GPIO.OUT) # setup the green light



def request_text(channel):
    # print(user_logged['user_name'])
#     data = api.request_quotes()
#     print(data)
#     print('Button Pressed')
#     GPIO.output(14, GPIO.HIGH)
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 1:
        led.all_off()
        led.blue_on()
        current_user.resources -= 1
        activity_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        new_activity = Activity(uid=user_logged['user_uid'], date=activity_time.split(' ')[0],
                                time=activity_time.split(' ')[1], query='text')
        db.session.add(new_activity)
        db.session.commit()
        print('You spend 1 point.')
        user_logged['user_choice'] = 'text'
        user_logged['user_resources'] = current_user.resources
        user_logged['message'] = 'You queried a text message from us. This costs you one.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        text_requested = api.request_tweets()
        printer.print_tweets()
        print(text_requested)
        led.all_on()
        user_logged['message'] = 'Your query is finished. What else do you want from us?'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')

    else:
        user_logged['message'] = 'You cannot afford a text message.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        print('You cannot afford a text message.')
#     else:
#         print("You can't afford a text message!")

def request_image(channel):
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 2:
        # printer.print_tweets()
        print("You spent 2 points for an image!")
        current_user.resources -= 2
        new_activity = Activity(uid=user_logged['user_uid'], date=activity_time.split(' ')[0],
                                time=activity_time.split(' ')[1], query='image')
        db.session.add(new_activity)
        db.session.commit()
        user_logged['user_choice'] = 'image'
        user_logged['user_resources'] = current_user.resources
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
    else:
        user_logged['message'] = 'You cannot afford an image.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        print('You cannot afford an image message.')

def request_sound(channel):
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 3:
        led.all_off()
        led.yellow_on()
        # printer.print_tweets()
        print("You spent 3 points for a sound message!")

        current_user.resources -= 3
        activity_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        new_activity = Activity(uid=user_logged['user_uid'], date=activity_time.split(' ')[0],
                                time=activity_time.split(' ')[1], query='sound')
        db.session.add(new_activity)
        db.session.commit()
        led.all_on()
        user_logged['user_resources'] = current_user.resources
        user_logged['message'] = 'You queried a sound message. This costs you three.'
        user_logged['user_choice'] = 'sound'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        sound.play_random_sound()
        user_logged['message'] = 'Your query is finished. What else do you want from us?'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')

    else:
        user_logged['message'] = 'You cannot afford a sound message.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        print('You cannot afford a sound message.')

def request_video(channel):
    current_user = User.query.filter_by(username=user_logged['user_name']).first()
    if current_user.resources >= 5:
        led.all_off()
        led.red_on()
        print("You spent 5 points for a video!")
        current_user.resources -= 5
        activity_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        # write something here
        new_activity = Activity(uid=user_logged['user_uid'], date=activity_time.split(' ')[0],
                                time=activity_time.split(' ')[1], query='video')
        db.session.add(new_activity)
        db.session.commit()
        led.all_on()
        user_logged['user_resources'] = current_user.resources
        user_logged['user_choice'] = 'video'
        user_logged['message'] = 'You queried a video from us. This costs all your points.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
    else:
        print('You cannot afford a video.')
        user_logged['message'] = 'You cannot afford a video.'
        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')



GPIO.add_event_detect(18, GPIO.FALLING, callback=request_text)
GPIO.add_event_detect(23, GPIO.FALLING, callback=request_image)
GPIO.add_event_detect(16, GPIO.FALLING, callback=request_sound)
GPIO.add_event_detect(12, GPIO.FALLING, callback=request_video)

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
        led.all_on()
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
            user_logged['message'] = 'What do you want to query from us?'

        socketio.emit('server_response', {'data': user_logged}, namespace='/conn')
        print(user_logged['user_name'], time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

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

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64))
    date = db.Column(db.String(64))
    time = db.Column(db.String(64))
    query = db.Column(db.String(64))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Activity=Activity)

if __name__ == '__main__':
    socketio.run(app, debug=True)
