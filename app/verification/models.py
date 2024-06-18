import os
import cv2
import cvzone
import joblib
import numpy as np
from converter import Converter
from cvzone.PlotModule import LivePlot
from cvzone.FaceMeshModule import FaceMeshDetector


from django.db import models
from django.core.files import File
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings


from celery import chain, shared_task

from authentication.models import Profile

# Create your models here.


class TaskEyeBlink(models.Model):
    expected_count = models.IntegerField()
    detected_count = models.IntegerField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"TaskEyeBlink {self.id}"


class VerificationTask(models.Model):
    task_choices = [
        ('eye_blink', 'Eye Blink'),
        # ('lip_movement', 'Lip Movement'),
    ]
    original_video = models.FileField(
        upload_to='original_videos/', null=True, blank=True)
    is_original_video_converted = models.BooleanField(default=False)
    processed_video = models.FileField(
        upload_to='processed_videos/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=task_choices)
    status = models.CharField(max_length=20, choices=[
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], null=True, blank=True)
    task_id = models.PositiveIntegerField()

    def __str__(self):
        return f"VerificationTask(id={self.id}, task_type='{self.task_type}', user='{self.user.username}', status='{self.status}'"


@shared_task
def detect_eye_blink(id):
    verificationTask = VerificationTask.objects.get(id=id)
    videoRecording = verificationTask.original_video
    videoPath = videoRecording.path

    LOGIC_REGRESSION_PATH = os.path.join(
        settings.BASE_DIR, 'ml_model', 'logic_regression.joblib')
    clf = joblib.load(LOGIC_REGRESSION_PATH)
    detector = FaceMeshDetector(maxFaces=1)
    plotY = LivePlot(640, 360, [-.5, 1.5], invert=True)
    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161,
              130, 243, 463, 286, 257, 260, 359, 339, 253, 256]

    # output_video_path = os.getcwd()

    video_dir = os.path.dirname(os.path.dirname(videoPath))
    converted_dir = os.path.join(video_dir, "processed_eye_blink")
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)
    video_file_name = os.path.basename(videoPath)
    output_video_path = os.path.join(converted_dir, video_file_name)

    cap = cv2.VideoCapture(videoPath)
    # Get information about the input video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * 2
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    # You can also use 'XVID', 'MJPG', etc.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(
        output_video_path, fourcc, fps, (frame_width, frame_height))

    blinkCounter = 0
    framecnt = 0
    left_eye_queue = []
    right_eye_queue = []
    last_predicted = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        img, faces = detector.findFaceMesh(img, draw=False)
        framecnt += 1
        if faces:
            face = faces[0]

            for id in idList:
                cv2.circle(img, face[id], 1, (255, 0, 255), cv2.FILLED)
            cv2.line(img, face[159],  face[23], (0, 200, 0), 1)
            cv2.line(img,  face[130], face[243], (0, 200, 0), 1)
            cv2.line(img, face[386], face[253], (0, 200, 0), 1)
            cv2.line(img, face[463], face[359], (0, 200, 0), 1)

            lefty1, _ = detector.findDistance(face[374], face[385])
            lefty2, _ = detector.findDistance(face[373], face[386])
            leftx, _ = detector.findDistance(face[33], face[133])
            A = lefty1
            B = lefty2
            C = leftx
            lefty1, _ = detector.findDistance(face[144], face[159])
            lefty2, _ = detector.findDistance(face[145], face[158])
            leftx, _ = detector.findDistance(face[263], face[362])
            D = lefty1
            E = lefty2
            F = leftx
            left_eye_aspect_ratio = (A + B) / (C)
            right_eye_aspect_ratio = (D + E) / (F)

            left_eye_queue.append(left_eye_aspect_ratio)
            right_eye_queue.append(right_eye_aspect_ratio)

            left_predictions = 0
            right_predictions = 0
            blink_now = 0

            if len(left_eye_queue) > 8:
                left_eye_queue.pop(0)
                q = np.array([left_eye_queue])
                left_predictions = clf.predict(q)[0]
            if len(right_eye_queue) > 8:
                right_eye_queue.pop(0)
                q = np.array([right_eye_queue])
                right_predictions = clf.predict(q)[0]

            if (left_predictions == 1) or (right_predictions == 1):
                blink_now = 1
                if last_predicted == 0:
                    blinkCounter += 1
                color = (0, 200, 0)
            else:
                color = (255, 0, 255)

            last_predicted = blink_now
            cvzone.putTextRect(
                img, f'{blinkCounter}', (50, 50), colorR=color)
            imgPlot = plotY.update(blink_now, color)
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        # cv2.imshow("Image", imgStack)
        # key = cv2.waitKey(5)
        output_video.write(imgStack)

        # if key == ord('x') or key == ord('X'):
        #     break

    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print(f"{framecnt=}, {blinkCounter=}")

    # Create a new VideoRecording object
    processed_video_recording = verificationTask.processed_video
    processed_video_key = os.path.basename(output_video_path)
    with open(output_video_path, 'rb') as f:
        processed_video_recording.save(processed_video_key, File(f), save=True)

    if os.path.exists(output_video_path):
        os.remove(output_video_path)  # Remove the file itself

        # Optionally, remove the directory if it's empty after file removal
        dir_path = os.path.dirname(output_video_path)
        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)  # Remove the directory if it's empty

    taskEyeBlink = TaskEyeBlink.objects.get(id=verificationTask.task_id)
    taskEyeBlink.detected_count = blinkCounter
    taskEyeBlink.accuracy = min(taskEyeBlink.expected_count, taskEyeBlink.detected_count) / \
        max(taskEyeBlink.expected_count, taskEyeBlink.detected_count)*100.0
    taskEyeBlink.save()
    verificationTask.save()

    return verificationTask.id


@shared_task
def video_conversion(id):
    verificationTask = VerificationTask.objects.get(id=id)
    videoRecording = verificationTask.original_video
    input_file_key = videoRecording.name.removeprefix('original_videos/')
    input_file_path = videoRecording.path
    output_file_path = os.path.splitext(input_file_path)[0] + '_converted.mp4'
    c = Converter()
    info = c.probe(input_file_path)
    convert = c.convert(input_file_path, output_file_path, {
        'format': 'mp4',
        'video': {
            'codec': 'hevc',
            'width': info.video.video_width,
            'height': info.video.video_height,
            'fps': info.video.video_fps
        }})
    for timecode in convert:
        pass
    if os.path.exists(input_file_path):
        os.remove(input_file_path)
    with open(output_file_path, 'rb') as f:
        verificationTask.is_original_video_converted = True
        videoRecording.save(input_file_key, File(f), save=True)
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    return id


@shared_task
def update_profile_verification_if_passed(id):
    task = VerificationTask.objects.get(id=id)
    if task.task_type == 'eye_blink':
        eye_blink_task = TaskEyeBlink.objects.get(id=task.task_id)
        if (eye_blink_task.accuracy >= settings.LIVELINESS_PASSED_PERCENTAGE):
            task.status = 'passed'
            profile = Profile.objects.get(user=task.user)
            profile.is_verified = True
            profile.save()
            task.save()


@receiver(models.signals.post_save, sender=VerificationTask)
def eye_blink_video_upload_post_processing(sender, instance, created, **kwargs):
    if instance.original_video and (not instance.is_original_video_converted):
        if instance.task_type == 'eye_blink':
            task_chain = chain(video_conversion.s(instance.id)
                               | detect_eye_blink.s()
                               | update_profile_verification_if_passed.s()
                               )
            task_chain.apply_async()
