from django import template
from django.contrib.auth.models import Group
from authentication.models import Profile
from notification.models import UserNotification

register = template.Library()


@register.simple_tag
def fetch_notifications(user):
    notifications = UserNotification.objects.filter(user=user, read=False)
    return notifications


@register.simple_tag
def fetch_unread_notificaton_count(user):
    unread_notification_count = UserNotification.objects.filter(
        user=user, read=False).count()
    return unread_notification_count


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter
def calculate_duration(login_time, logout_time):
    if login_time and logout_time:
        duration = logout_time - login_time
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours} hours, {minutes} minutes"
    else:
        return "N/A"


@register.filter
def is_profile_verified(user):
    print(f"{user=}")
    try:
        profile = Profile.objects.get(user=user)
        return profile.is_verified
    except Profile.DoesNotExist:
        return False
