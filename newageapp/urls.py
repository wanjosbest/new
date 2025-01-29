from django.urls import path
from .import views

urlpatterns =[
     path("api/register-user/", views.user_create, name="create-user"),
   
]
