from flask import Flask, render_template
from flask_socketIO import SocketIO, emit
from threading import Lock
from serial_reader import user_logged_uid, user_logged_name

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomprecision'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

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
        t = {
            'user_uid': user_logged_uid,
            'user_name': user_logged_name
        }

        socketio.emit('server_response', {'data': t}, namespace='/conn')


if __name__ == '__main__':
    socketio.run(app, debug=True)