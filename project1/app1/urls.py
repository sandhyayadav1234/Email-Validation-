
from django.urls import path
from .views import Register,UserLogin,ProfileView,UserCangePassword,SendPasswordRestEmail,UserPasswordRestView
urlpatterns = [
   path('register/',Register.as_view(),name='register'),
   path('login/',UserLogin.as_view(),name='login'),
   path('profile/',ProfileView.as_view(),name='Profile '),
   path('ChangePassword/',UserCangePassword.as_view(),name='change_pass '),
   path('SendResetPassword/',SendPasswordRestEmail.as_view(),name='ResetPassword '),
   path('ResetPassword/<uuid>/<token>/',UserPasswordRestView.as_view(),name='UserPassword '),
]
