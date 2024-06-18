from django.urls import path
from authentication import views as auth_app

urlpatterns = [
    path('login', auth_app.user_login, name='login'),
    path('logout', auth_app.user_logout, name='logout'),
    #     path('create', auth_app.register, name='register'),
    path('forget-password/', auth_app.ForgetPassword, name="forget_password"),
    path('change-password/<token>/',
         auth_app.ChangePassword, name="change_password"),
    path('change-user-password/',
         auth_app.ChangePasswordByUser, name="change_user_password"),
    path('update-profile/',
         auth_app.update_profile, name="update_profile"),
]
