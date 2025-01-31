from django.shortcuts import render, redirect,HttpResponse
from .mongo import users_collection
from .forms import UserForm
from pymongo import MongoClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
import jwt
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from .serializers import (Userregister)
import hashlib # for hashing password
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Insert new user into MongoDB
            user_data = form.cleaned_data
            users_collection.insert_one(user_data)
            return HttpResponse("Added Successfully")
    else:
        form = UserForm()
    return render(request, 'user_form.html',{"form":form})

#user register
class RegisterView(APIView):
    PERMISSION_CLASSES = [AllowAny]

    def post(self, request):
       serializer = Userregister(data = request.data)
       if serializer.is_valid():
          firstname = serializer.validated_data["firstname"]
          lastname = serializer.validated_data["lastname"]
          email = serializer.validated_data["email"]
          password = serializer.validated_data["password"]
          username = serializer.validated_data["username"]
          address = serializer.validated_data["address"]
          dob = serializer.validated_data["dob"]
          course = serializer.validated_data["course"]
          phonenumber = serializer.validated_data["phonenumber"]
          gender = serializer.validated_data["gender"]
          agreed_termsconditions = serializer.validated_data["agreed_termsconditions"]
          # check if the user exist
          if users_collection.find_one({"username":username}):
             return Response ("user already exist", status = status.HTTP_400_BAD_REQUEST)
          hashed_password = hashlib.sha256(password.encode()).hexdigest()

          #create user and save 
          user_data = {
            "firstname":firstname,
            "lastname":lastname,
            "email": email,
            "password": hashed_password,
            "username":username,
            "address":address,
            "course":course,
            "dob":dob,
            "phonenumber":phonenumber,
            "gender":gender,
            "agreed_termsconditions":agreed_termsconditions
          }
         
          result = users_collection.insert_one(user_data)
          user_data["_id"] = result.inserted_id  # Add the ObjectId after insertion


          payload = {
            "user_id": str(user_data['_id']),
            "exp": datetime.utcnow() + timedelta(hours = 1),
            "iat": datetime.utcnow(),
          }
          
          token = jwt.encode(payload, settings.SECRET_KEY) #token created
          return Response ({"message":"Usercreateated successfully", 
                            "token":token}, status.HTTP_200_OK)
       return Response(status = status.HTTP_400_BAD_REQUEST)                    

class LoginView(APIView):
    PERMISSION_CLASSES = [AllowAny]# allow anybody to login
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # now authenticate the user 
        user = users_collection.find(request, username= username, password = password )
        if user is None:
            return Response({"error: invalid credentials"}, status = 400)
        #create data to encode
        payload = {
            "user_id": str(user.id),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
        }
        #encode
        token = jwt.encode(payload, settings.SECRET_KEY)
        return Response({"token":token}, status = 200 )

