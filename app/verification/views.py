import random

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.static import serve
from django.conf import settings
from django.contrib.auth.decorators import login_required

from web_project import TemplateLayout
from verification.models import VerificationTask, TaskEyeBlink


@login_required
def watch_processed_video(request, task_id):
    context = TemplateLayout.init(request, {})
    task = get_object_or_404(VerificationTask, pk=task_id)
    obj = None
    if (task.task_type == 'eye_blink'):
        obj = TaskEyeBlink.objects.get(id=task.task_id)
    context.update({
        'task': task,
        'task_details': obj
    })
    return render(request, 'verification/task-deatails.html', context)


@login_required
def verify(request):
    context = TemplateLayout.init(request, {})
    tasks = VerificationTask.task_choices
    chosen_task = tasks[random.randint(0, len(tasks)-1)]

    if chosen_task[0] == 'eye_blink':
        eye_blink_task = TaskEyeBlink.objects.create(
            expected_count=random.randint(3, 7))
        new_task = VerificationTask.objects.create(
            user=request.user,
            task_type=chosen_task[0],
            task_id=eye_blink_task.id
        )
        context.update({
            'task_id': new_task.id,
            'expected_count': eye_blink_task.expected_count
        })
        return render(request, 'verification/eye_blink_verification.html', context)

    return render(request, 'verification/eye_blink_verification.html', context)


@login_required
def save_eye_blink_recording(request):
    if request.method == 'POST' and request.FILES['video_blob']:
        video_file = request.FILES['video_blob']
        task_id = int(request.POST.get('task_id'))

        print(f"{task_id=}")
        verificationTask = VerificationTask.objects.get(id=task_id)
        verificationTask.original_video.save(
            video_file.name, video_file, save=True)
        messages.success(
            request, "Keep an eye on notification to see verification results.")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})


@login_required
def video_record(request):
    context = TemplateLayout.init(request, {})

    # Update the context

    return render(request, 'common/video_record.html', context)


# @login_required
# def save_recording(request):
#     print('-----------------saving recording ----------------')
#     if request.method == 'POST' and request.FILES['video_blob']:
#         video_file = request.FILES['video_blob']
#         title = request.POST.get('title', 'Untitled')
#         video_recording = VideoRecording(
#             video_file=video_file,
#             user=request.user
#         )
#         video_recording.save()
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'failed'})
