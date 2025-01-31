from django.urls import path
from .import views
from newageapp.views import RegisterView,LoginView

urlpatterns =[
     path("api/register-user/", RegisterView.as_view(), name="register"),
     path("api/login-user/", LoginView.as_view(), name="login"),
    
   
]
