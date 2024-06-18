from django.urls import path
from verification import views

urlpatterns = [
    path('', views.verify, name='verify'),
    # path('video_record/', views.video_record, name='video_record'),
    # path('save_recording/', views.save_recording, name='save_recording'),
    path('save_eye_blink_recording/', views.save_eye_blink_recording,
         name='save_eye_blink_recording'),
    path('tasks/<int:task_id>/',
         views.watch_processed_video, name='verification_task_details'),



]
