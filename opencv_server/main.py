from flask import Flask, Response, render_template, make_response
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Yield the frame as a response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # Your video feed logic here

    response = Response(generate(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
