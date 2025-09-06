from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),            # Dashboard page
    path('video_feed/', views.video_feed, name='video_feed'),  # Streaming webcam feed
    path('posture_status/', views.posture_status, name='posture_status'),  # Current posture JSON
]
