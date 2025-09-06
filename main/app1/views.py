from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from .utlis import get_frame_and_status, current_status
from .models import DailyPostureScore
import cv2, time
from django.contrib.auth.decorators import login_required

last_good_start = None
last_bad_time = 0   # ✅ new: track last time we deducted bad

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

@login_required
def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

@login_required
def posture_status(request):
    global last_good_start, last_bad_time

    user = request.user
    today = now().date()
    score_obj, _ = DailyPostureScore.objects.get_or_create(user=user, date=today)

    if current_status == "Good":
        if last_good_start is None:
            last_good_start = time.time()
        else:
            elapsed = time.time() - last_good_start
            if elapsed >= 5:  
                score_obj.score += 2
                score_obj.save()
                last_good_start = None
    elif current_status == "Bad":
        now_time = time.time()
        if now_time - last_bad_time >= 10:  
            score_obj.score -= 1
            score_obj.save()
            last_bad_time = now_time
        last_good_start = None  

    return JsonResponse({"status": current_status, "score": score_obj.score})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
