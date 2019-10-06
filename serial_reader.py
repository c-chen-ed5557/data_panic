import serial

user_list = {
    '39 70 17 2D': 'C.CHEN',
    '8B 15 D6 15': 'F.XUE'
}

user_logged_uid = None
user_logged_name = ''
log_status = False

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    ser.readline()
    user_id = ser.readline().decode('utf-8')

    for k, v in user_list:
        if k in user_id:
            user_logged_uid = k
            user_logged_name = v

