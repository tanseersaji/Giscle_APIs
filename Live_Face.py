from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import time

token = 'Paste Your Token'

g_url = 'http://api.giscle.ml'


def extract_data(args):
    
    print(args)

socketio = SocketIO(g_url, 80, LoggingNamespace)

socketio.emit('authenticate', {'token': token})

cam = cv2.VideoCapture(0)

frame_count = 1

while True:
    global t
    t = time.time()
    ret, frame = cam.read()
    if not ret:
        continue
    frame = cv2.resize(frame, (900, 600))
    encoded, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer)
    encoded_frame = encoded_frame.decode('utf-8')
    socketio.emit('faged', {'data': encoded_frame})
    socketio.on('response', extract_data)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.imshow("frame",frame)
    socketio.wait(0.0001)
    print(time.time() - t)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

socketio.disconnect()
cam.release()
