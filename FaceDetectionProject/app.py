from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import cv2
import os
import time

app = FastAPI()

# ✅ FIXED spelling
templates = Jinja2Templates(directory="templates")

# Create screenshots folder
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

camera = cv2.VideoCapture(0)

last_capture_time = 0
cooldown = 5
img_count = 0


def generate_frames():
    global last_capture_time, img_count

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        face_detected = False

        for (x, y, w, h) in faces:
            face_detected = True
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        face_count = len(faces)
        cv2.putText(frame, f'Faces: {face_count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # ✅ Screenshot logic
        current_time = time.time()

        if face_detected and (current_time - last_capture_time > cooldown):
            img_name = f"screenshots/face_{img_count}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Screenshot saved: {img_name}")

            img_count += 1
            last_capture_time = current_time

        # ✅ Always encode & yield (IMPORTANT)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/video")
def video():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')