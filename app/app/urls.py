from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from web_project.views import SystemView
from core.views import dashboard, under_maintenance
from notification.consumers import NotificationConsumer
from notification import views as notification_app


urlpatterns = [
    #     path("notification", notification_app.notification_page_view,
    #          name="notification_page"),
    path('admin/', admin.site.urls, name='admin_dashboard'),
    # path('captcha/', include('captcha.urls')),
    path('under_maintenance', under_maintenance, name='under_maintenance'),


    # notification
    path('view_all_notification', notification_app.read_all_notification,
         name="read_all_notification"),

    # auth
    path('auth/', include('authentication.urls')),

    path('verification/', include('verification.urls')),


    path('', dashboard, name='dashboard'),

]

# websocket_urlpatterns = [
#     path("ws/notifications/", NotificationConsumer.as_asgi())
# ]


# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = SystemView.as_view(
    template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(
    template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(
    template_name="pages_misc_error.html", status=500)
