from flask import Flask, render_template, Response
from flask_basicauth import BasicAuth
from config import Config

# select the camera you want to interface
# if you are using pi camera
# then uncomment the second import
# and comment the first one

from camera.web_cam import VideoCamera
# from camera.pi_cam import VideoCamera


app = Flask(__name__)
app.config.from_object(Config)
auth = BasicAuth(app)


@auth.required
@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        # frame = camera.get_object(classifier=cv2.CascadeClassifier('models/facial_recognition_model.xml'))
        # frame = camera.get_frame()
        frame = camera.get_mask()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@auth.required
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


