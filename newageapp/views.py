
from django.shortcuts import render, redirect,HttpResponse
from .forms import UserForm
from pymongo import MongoClient
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.http import JsonResponse
import jwt
import bcrypt
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from .serializers import (Studentregister,Tutorregister,Adminregister,Affiliateregister, AffiliateWalletSerializer)
from .models import (Student, Admin, Tutor, affiliate, available_courses, live_classes, student_attendance, anouncements, assignments,
course_timetables, exam_timetables, AffiliateWallet)
import hashlib # for hashing password
from django.contrib.auth.models import User
from .mongo import db
from .permissions import IsAdmin, IsAffiliate, IsTutor,IsStudent
affiliate_collection = db["affiliate"]
student_collection = db["student"]
tutor_collection = db["tutor"]
available_courses_collection = db['available_courses']
live_classes_collection = db['live_classes']
student_attendance_collection = db['student_attendance']
announcements_collection = db['announcements']
assignments_collection = db['assignments']
course_timetables_collection = db['course_timetables']
admin_collection = db["admin"]
users_collection = db["USERS"]
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


def scrape_view(request):
    url = "https://best9ja.com.ng/how-to-upload/"  # Change to the target URL
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract relevant data (modify as needed)
        titles = soup.find_all("h2")  # Example: Extracting all h2 tags
        
        extracted_data = [title.get_text() for title in titles]

        return render(request, "data.html", {"datain": extracted_data})

    return render(request, "data.html", {"data": ["Failed to retrieve data"]})
# hash password with bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


#Admin CRUD
#Admin  register
@api_view(["POST"])
@permission_classes([AllowAny])
def RegisterAdmin( request):
    serializer = Adminregister(data = request.data)
    if serializer.is_valid():
       firstname = serializer.validated_data["firstname"]
       lastname = serializer.validated_data["lastname"]
       email = serializer.validated_data["email"]
       password = serializer.validated_data["password"]
       hashed_password = hash_password(password) #hash password before saving using the bcrypt hashing function
       username = serializer.validated_data["username"]
       address = serializer.validated_data["address"]
       dob = serializer.validated_data["dob"]
       course = serializer.validated_data["course"]
       phonenumber = serializer.validated_data["phonenumber"]
       gender = serializer.validated_data["gender"]
        # check if the Admin exist
        
       if admin_collection.find_one({"username":username}) or student_collection.find_one({"username":username}) or affiliate_collection.find_one({"username":username}) or Tutor_collection.find_one({"username":username}):
          return Response ("User already exist use unique username and email", status = status.HTTP_400_BAD_REQUEST)
       studentreg = Admin(firstname=firstname, lastname=lastname, username=username, email=email, password=hashed_password,course=course,address=address,dob=dob,phonenumber=phonenumber,gender=gender)
       studentreg.save()
       return Response({"message": "AdminRegistered Succesfully"},status = status.HTTP_201_CREATED)   
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)                    

# get all Admin
@api_view(["GET"])
@permission_classes([IsAdmin])
def get_admin_list(request):
    if request.method == "POST":
        get_admin = Admin.get_all_admin()
        return Response(get_admin, status = status.HTTP_200_OK)
    return Response( status = status.HTTP_400_BAD_REQUEST)

# update admin
@permission_classes([IsAdmin])
@api_view(["POST"])
def update_adminview(request, id):
    if request.method == "POST":
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

        Admin.update_admin(id,firstname, lastname, username, email, password,course,address,dob,phonenumber,gender)
        return Response({"message": "Admin Updated"}, status = status.HTTP_200_OK)
#delete student
@permission_classes([IsAdmin])
@api_view(["DELETE"])
def delete_adminview(request, id):
    if request.method == "DELETE":
       Admin.delete_admin(id)
       return Response({"message":"Admin deleted"}, status = status.HTTP_200_OK)
    return Response({"error":"Only delete method allowed here please"}, status = status.HTTP_400_BAD_REQUEST)


#Affiliate CRUD
#Affiliate  register
@api_view(["POST"])
@permission_classes([AllowAny])
def RegisterAffiliate(request):
    serializer = Affiliateregister(data = request.data)
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
       hashed_password = hash_password(password) #hash password before saving using the bcrypt hashing function
        # check if the Affiliate exist
       if admin_collection.find_one({"username":username}) or student_collection.find_one({"username":username}) or affiliate_collection.find_one({"username":username}) or Tutor_collection.find_one({"username":username}):
          return Response ("User already exist use unique username and email", status = status.HTTP_400_BAD_REQUEST)
      
       affiliatereg = affiliate(firstname=firstname, lastname=lastname, username=username, email=email, password=hashed_password,course=course,address=address,dob=dob,phonenumber=phonenumber,gender=gender)
       affiliatereg.save()
       return Response({"message":"Affiliate Created Successfully"},status = status.HTTP_201_CREATED)   
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)                    

# get all Affiliate
@permission_classes([IsAdmin])
@api_view(["GET"])
def get_affiliate_list(request):
    if request.method == "POST":
        get_affiliate = affiliate.get_all_affiliate()
        return Response(get_affiliate, status = status.HTTP_200_OK)
    return Response( status = status.HTTP_400_BAD_REQUEST)

# update affiliate
@permission_classes([IsAdmin, IsAffiliate])
@api_view(["POST"])
def update_affiliateview(request, id):
    if request.method == "POST":
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
        affiliate.update_affiliate(id,firstname, lastname, username, email, password,course,address,dob,phonenumber,gender)
        return Response({"message": "Affiliate Updated"}, status = status.HTTP_200_OK)
#delete affiliate
@permission_classes([IsAdmin, IsAffiliate])
@api_view(["DELETE"])
def delete_affiliateview(request, id):
    if request.method == "DELETE":
       affiliate.delete_affiliate(id)
       return Response({"message":"affiliate deleted"}, status = status.HTTP_200_OK)
    return Response({"error":"Only delete method allowed here please"}, status = status.HTTP_400_BAD_REQUEST)



#Student CRUD
@api_view(["POST"])
@permission_classes([AllowAny])
def RegisterView( request):
    serializer = Studentregister(data = request.data)
    if serializer.is_valid():
        firstname = serializer.validated_data["firstname"]
        lastname = serializer.validated_data["lastname"]
        email = serializer.validated_data["email"]
        username = serializer.validated_data["username"]
        address = serializer.validated_data["address"]
        dob = serializer.validated_data["dob"]
        course = serializer.validated_data["course"]
        phonenumber = serializer.validated_data["phonenumber"]
        gender = serializer.validated_data["gender"]
        password = serializer.validated_data["password"]
        hashed_password = hash_password(password) #hash password before saving using the bcrypt hashing function
        # check if the user exist
        
        if admin_collection.find_one({"username":username}) or student_collection.find_one({"username":username}) or affiliate_collection.find_one({"username":username}) or Tutor_collection.find_one({"username":username}):
          return Response ("User already exist use unique username and email", status = status.HTTP_400_BAD_REQUEST)
        studentreg = Student(firstname=firstname, lastname=lastname, username=username, email=email, password=hashed_password,course=course,address=address,dob=dob,phonenumber=phonenumber,gender=gender)
        studentreg.save()
        return Response({"message": "Student registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   

# get all students
@permission_classes([IsAdmin])
@api_view(["GET"])
def get_students_list(request):
    if request.method == "POST":
        get_stu = Student.get_all_students()
        return Response(get_stu, status = status.HTTP_200_OK)
    return Response( status = status.HTTP_400_BAD_REQUEST)

# update student
@permission_classes([IsAdmin])
@api_view(["POST"])
def update_student(request, id):
    if request.method == "POST":
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

        Student.update_student(id,firstname, lastname, username, email, password,course,address,dob,phonenumber,gender)
        return Response({"message": "Student Updated"}, status = status.HTTP_200_OK)
#delete student
@permission_classes([IsAdmin])
@api_view(["DELETE"])
def delete_student(request, id):
    if request.method == "DELETE":
       Student.delete_student(id)
       return Response({"message":"student deleted"}, status = status.HTTP_200_OK)
    return Response({"error":"Only delete method allowed here please"}, status = status.HTTP_400_BAD_REQUEST)

#CRUD Tutors

#Tutor  register
@api_view(["POST"])
@permission_classes([IsAdmin])
def RegisterTutor(request):
    serializer = Tutorregister(data = request.data)
    if serializer.is_valid():
       firstname = serializer.validated_data["firstname"]
       lastname = serializer.validated_data["lastname"]
       email = serializer.validated_data["email"]
       password = serializer.validated_data["password"]
       hashed_password = hash_password(password) #hash password before saving using the bcrypt hashing function
       username = serializer.validated_data["username"]
       address = serializer.validated_data["address"]
       dob = serializer.validated_data["dob"]
       course = serializer.validated_data["course"]
       phonenumber = serializer.validated_data["phonenumber"]
       gender = serializer.validated_data["gender"]
        # check if the user exist
       if admin_collection.find_one({"username":username}) or student_collection.find_one({"username":username}) or affiliate_collection.find_one({"username":username}) or Tutor_collection.find_one({"username":username}):
         return Response ("User already exist use unique username and email", status = status.HTTP_400_BAD_REQUEST)
       tutorreg = Tutor(firstname=firstname, lastname=lastname, username=username, email=email, password=hashed_password,course=course,address=address,dob=dob,phonenumber=phonenumber,gender=gender)
       tutorreg.save()
       return Response({"message":"Tutor created succesfully"},status = status.HTTP_201_CREATED)   
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)                    

# get all Tutors
@permission_classes([IsAdmin])
@api_view(["GET"])
def get_tutors_list(request):
    if request.method == "POST":
        get_tutor = Tutor.get_all_tutors()
        return Response(get_tutor, status = status.HTTP_200_OK)
    return Response( status = status.HTTP_400_BAD_REQUEST)

# update tutor
@permission_classes([IsAdmin,IsTutor])
@api_view(["POST"])
def update_tutorview(request, id):
    if request.method == "POST":
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

        Tutor.update_tutor(id,firstname, lastname, username, email, password,course,address,dob,phonenumber,gender)
        return Response({"message": "Tutor Updated"}, status = status.HTTP_200_OK)

#delete tutor
@permission_classes([IsAdmin])
@api_view(["DELETE"])
def delete_tutorview(request, id):
    if request.method == "DELETE":
       tutor.delete_tutor(id)
       return Response({"message":"Tutor deleted"}, status = status.HTTP_200_OK)
    return Response({"error":"Only delete method allowed here please"}, status = status.HTTP_400_BAD_REQUEST)




#all login

def get_tokens_for_user(user_id):
    """
    Generate JWT tokens 
    """
    refresh = RefreshToken()
    refresh["user_id"] = user_id  # Store user ID inside the token

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login Authentication with JWT
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = admin_collection.find_one({"username": username}) or student_collection.find_one({"username": username}) or  tutor_collection.find_one({"username": username}) or  affiliate_collection.find_one({"username": username})

    if not user:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    stored_hashed_password = user["password"].encode("utf-8")
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password):
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT token
    tokens = get_tokens_for_user(str(user["_id"]))  # Store MongoDB _id in JWT

    return Response({
        "message": "Login successful",
        **tokens,
    }, status=status.HTTP_200_OK)
#CRUD COURSES

@api_view(["POST"])
@permission_classes([IsAdmin])
def create_course(request):
    if request.method =="POST":
        print("User:", request.user)  # Debugging user object
        print("User Role:", getattr(request.user, "role", "No Role Found"))  # Debugging role
        author = request.data.get("author")
        title  = request.data.get("title")
        slug   = request.data.get("slug")
        savingdata = available_courses_collection(author, title, slug)
        savingdata.save()
        return Response({"message": "Course added"}, status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)
   
    

#view all courses
@permission_classes([AllowAny])
@api_view(["GET"])
def view_courses(request):
    if request.method =="GET":
        courses = available_courses.get_courses()
        return Response(courses, status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update course
@permission_classes([IsAdmin])
@api_view(["POST"])
def update_course(request, id):
    if request.method =="POST":
        author = request.data.get("author")
        title  = request.data.get("title")
        slug   = request.data.get("slug")
        savingdata = available_courses.update_course(id,author, title, slug)
        return Response(status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#delete course
@permission_classes([IsAdmin])
@api_view(["DELETE"])
def delete_course(request, id):
    if request.method =="DELETE":
        available_courses_collection.delete_course(id)
        return Response(status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)


# CRUD Live class

@permission_classes([IsAdmin,IsTutor])
@api_view(["POST"])
def create_live_class(request):
    if request.method =="POST":
        class_name = request.data.get("class_name")
        class_description = request.data.get("class_description")
        class_link = request.data.get("class_link")
        savingdata = live_classes(class_name, class_description, class_link)
        savingdata.save()
        return Response(status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# view live class details
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def view_live_class(request):
    if request.method =="GET":
        getdata = live_classes.view_live_class()
        return Response(getdata, status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update live class
@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def update_live_class(request):
    if request.method =="PUT":
        class_name = request.data.get("class_name")
        class_description = request.data.get("class_description")
        class_link = request.data.get("class_link")
        savingdata = live_classes.update_live_class(class_name, class_description, class_link)
        return Response( status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#delete live class
@permission_classes([IsAdmin, IsTutor])
@api_view(["DELETE"])
def delete_live_class(request,id):
    if request.method =="DELETE":
        live_classes.delete_live_class(id)
        return Response({"message": "Live class deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# styudent  class attendance
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def student_class_attendance(request):
    if request.method =="POST":
        student_email = request.data.get("student_email")  
        course_title = request.data.get("course_title") 
        savingdata = student_attendance(student_email, course_title)
        savingdata.save()
        return Response({"message": "attendance created"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#view all students that attend class
@permission_classes([IsAdmin,IsTutor])
@api_view(["GET"])
def view_student_class_attendance(request):
    if request.method =="GET":
        results = student_attendance.get_attendance()
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update student attendance
@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def update_student_class_attendance(request, student_email):
    if request.method =="PUT":
        student_email = request.data.get("student_email")  
        course_title = request.data.get("course_title") 
        savingdata = student_attendance.update_attendance(student_email, course_title) 
        return Response({"message": "attendance updated"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#delete student attendance
@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def delete_student_class_attendance(request, student_email):
    if request.method =="PUT":
        student_attendance.delete_student_attendance(student_email)
        return Response({"message": "attendance deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# CRUD anouncement

@permission_classes([IsAdmin,IsTutor])
@api_view(["POST"])
def create_anouncements(request):
    if request.method =="POST":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = anouncements(tutor, title, content)
        savingdata.save()
        return Response({"message": "ANOUNCEMENT CREATED"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# VIEW  single anouncement by id

@permission_classes([IsAuthenticated])
@api_view(["GET"])
def view_single_anouncement(request, id):
    if request.method =="GET":
        results = anouncements.view_anouncement(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update anouncement

@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def update_anouncements(request, id):
    if request.method =="PUT":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = anouncements.update_anouncement(id, tutor, title, content)
        return Response({"message": "anouncements Updated"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# delete Anouncement
@permission_classes([IsAdmin,IsTutor])
@api_view(["DELETE"])
def delete_anouncements(request, id):
    if request.method =="DELETE":
       anouncements.delete_anouncement(id)
       return Response({"message": "anouncements deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#CRUD Assignments

@permission_classes([IsAdmin, IsTutor])
@api_view(["POST"])
def create_class_assignment(request):
    if request.method =="POST":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = assignments(tutor, title, content)
        savingdata.save()
        return Response({"message": "assignment created"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# view assignment by id
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def view_class_assignment(request, id):
    if request.method =="GET":
        results = assignments.view_assignment(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update assignment

@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def update_class_assignment(request, id):
    if request.method =="PUT":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = assignments.update_assignment(id,tutor, title, content)
        return Response({"message": "assignment updated"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# delete assignment


@permission_classes([IsAdmin,IsTutor])
@api_view(["DELETE"])
def delete_class_assignment(request, id):
    if request.method =="DELETE":
        assignments.delete_assignment(id)
        return Response({"message": "assignment deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# CRUD Class timetable
@permission_classes([IsAdmin,IsTutor])
@api_view(["POST"])
def create_class_timetable(request):
    if request.method =="POST":
        tutor = request.data.get("tutor")
        course = request.data.get("course")
        class_link = request.data.get("class_link")
        savingdata = course_timetables(tutor,course, class_link)
        savingdata.save()
        return Response({"message": "time table created"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# view time table by id 

@permission_classes([IsAuthenticated])
@api_view(["GET"])
def view_class_timetable(request, id):
    if request.method =="GET":
        results = course_timetables.view_time_table(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update time table by id
@permission_classes([IsAdmin,IsTutor])
@api_view(["PUT"])
def update_class_timetable(request, id):
    if request.method =="PUT":
        tutor = request.data.get("tutor")
        course = request.data.get("course")
        class_link = request.data.get("class_link")
        course_timetables.update_time_table(id, tutor,course, class_link)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#delete classs timetable

@permission_classes([IsAdmin,IsTutor])
@api_view(["DELETE"])
def delete_class_timetable(request, id):
    if request.method =="DELETE":
        course_timetables.delete_timetable(id)
        return Response({"message":"time table deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#CRUD Exam timetables


@permission_classes([IsAdmin])
@api_view(["POST"])
def create_exam_timetable(request):
    if request.method =="POST":
        title = request.data.get("title")
        course = request.data.get("course")
        class_link = request.data.get("class_link")
        savingdata = exam_timetables(title, course,class_link)
        return Response({"message":" exam time table created"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

    # view exam timetable
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def view_exam_timetable(request, id):
    if request.method =="GET":
        results = exam_timetables.view_exam_time_table(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update exam timetable
@permission_classes([IsAdmin])
@api_view(["PUT"])
def update_exam_timetable(request, id):
    if request.method =="PUT":
        title = request.data.get("title")
        course = request.data.get("course")
        class_link = request.data.get("class_link")
        savingdata = exam_timetables.update_exam_time_table(id, title, course,class_link) 
        return Response({"message":"Exam timetable updated"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST) 

# delete exam timetable

@permission_classes([IsAdmin])
@api_view(["DELETE"])
def delete_exam_timetable(request, id):
    if request.method =="DELETE":
        exam_timetables.delete_exam_timetable(id)
        return Response({"message":"Exam timetable deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST) 

#CRUD AFFILIATE WALLET
@api_view(["GET"])
@permission_classes([IsAffiliate,IsAdmin])
def ViewAffiliateWallet(request):
    if request.method =="GET":
       affiliate_wallet = AffiliateWallet.get_all()
       serializer = AffiliateWalletSerializer(affiliate_wallet, many = True)
       return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({"error":"Bad request use GET Request onny"}, status = status.HTTP_400_BAD_REQUEST) 

@api_view(["POST"])
@permission_classes([IsAffiliate,IsAdmin])
def CreateAffiliateWallet(request):
    if request.method == "POST":
       serializer = AffiliateWalletSerializer( data = request.data)
       if serializer.is_valid():
          serializer.save()
          return Response({"message":" Congrations! AffWallet Created "}, status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request Use POST Request Only"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAdmin])
def UpdateAffiliateWallet(request):
    if request.method == "PUT":
        affiliate_wallet = AffiliateWallet.get_by_id(affiliate_id)
        if affiliate_wallet:
            serializer = AffiliateWalletSerializer(affiliate_wallet, data = request.data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error":"Bad request "}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Wallet Not Found "}, status = status.HTTP_404_NOT_FOUND)
    return Response({"error":"Bad request use PUT request only for Update "}, status = status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdmin])
def DeleteAffiliateWallet(request,username):
    if request.method =="DELETE":
       AffiliateWallet.delete_wallet(username)
       return Response({"message":"Wallet delete"},status = status.HTTP_200_OK)
    return Response({"message":"Use DELETE request only please"}, status = status.HTTP_400_BAD_REQUEST)

            
       
       
