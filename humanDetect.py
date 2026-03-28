from flask import Flask, request
from ultralytics import YOLO
import numpy as np
import cv2

app = Flask(__name__)
model = YOLO("yolov8n.pt")

@app.route("/detect", methods=["POST"])
def detect():
    img_array = np.frombuffer(request.data, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    results = model(frame)
    
    persons = [r for r in results[0].boxes.cls if int(r) == 0]
    return {"persons_detected": len(persons)}

app.run(host="0.0.0.0", port=5000)


// ESP32
HTTPClient http;
http.begin("http://192.168.1.x:5000/detect");
http.addHeader("Content-Type", "image/jpeg");
http.POST(imageBuffer, imageSize);

pip install ultralytics