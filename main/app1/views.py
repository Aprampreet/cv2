from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from .utlis import get_frame_and_status, current_status
import cv2

def gen_frames():
    while True:
        frame, _ = get_frame_and_status()
        if frame is None:
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def posture_status(request):
    return JsonResponse({"status": current_status})

def dashboard(request):
    return render(request, "dashboard.html")