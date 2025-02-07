from django.shortcuts import render, redirect,HttpResponse
from .forms import UserForm
from pymongo import MongoClient
from rest_framework.views import APIView, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import authenticate
import jwt
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from .serializers import (Studentregister)
from .models import (Student, available_courses, live_classes, student_attendance, announcements, assignments,
course_timetables, exam_timetables)
import hashlib # for hashing password
from .mongo import db
student_collection = db["student"]
available_courses_collection = db['available_courses']
live_classes_collection = db['live_classes']
student_attendance_collection = db['student_attendance']
announcements_collection = db['announcements']
assignments_collection = db['assignments']
course_timetables_collection = db['course_timetables']
#Student CRUD
#Student  register
class RegisterView(APIView):
    PERMISSION_CLASSES = [AllowAny]

    def post(self, request):
       serializer = Studentregister(data = request.data)
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
        # check if the user exist
          student_collection = db["student"]
          if users_collection.find_one({"username":username}):
             return Response ("user already exist", status = status.HTTP_400_BAD_REQUEST)
          password = hashlib.sha256(password.encode()).hexdigest() #hash password before saving
          
          studentreg = Student(firstname, lastname, username, email, password,course,address,dob,phonenumber,gender)
          studentreg.save()
          return Response(status = status.HTTP_201_CREATED)   
       return Response(status = status.HTTP_400_BAD_REQUEST)                    

# get all students
@PERMISSION_CLASSES([IsAdminUser])
@api_view(["GET"])
def get_students_list(request):
    if request.method == "POST":
        get_stu = Student.get_all_students()
        return Response(get_stu, status = status.HTTP_200_OK)
    return Response( status = status.HTTP_400_BAD_REQUEST)

# update student
@PERMISSION_CLASSES([IsAdminUser])
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
@PERMISSION_CLASSES([IsAdminUser])
@api_view(["DELETE"])
def delete_student(request, id):
    if request.method == "DELETE":
       Student.delete_student(id)
       return Response({"message":"student deleted"}, status = status.HTTP_200_OK)
    return Response({"error":"Only delete method allowed here please"}, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    PERMISSION_CLASSES = [AllowAny]# allow anybody to login
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # now authenticate the user 
        user = student_collection.find(request, username= username, password = password )
        if user is None:
            return Response({"error: invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)
        #create data to encode
        payload = {
            "user_id": str(user.id),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
        }
        #encode
        token = jwt.encode(payload, settings.SECRET_KEY)
        return Response({"token":token}, status = 200 )

#CRUD COURSES
@permission_classes([IsAdminUser])
@api_view(["POST"])
def create_course(request):
    if request.method =="POST":
        author = request.data.get("author")
        title  = request.data.get("title")
        slug   = request.data.get("slug")
        savingdata = available_courses_collection(author, title, slug)
        savingdata.save()
        return Response({"message": "Course added"}, status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#view all courses
@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_courses(request):
    if request.method =="GET":
        courses = available_courses.get_courses()
        return Response(courses, status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update course
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_course(request, id):
    if request.method =="DELETE":
        available_courses_collection.delete_course(id)
        return Response(status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)


# CRUD Live class

@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_live_class(request):
    if request.method =="GET":
        getdata = live_classes.view_live_class()
        return Response(getdata, status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update live class
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_live_class(request,id):
    if request.method =="DELETE":
        live_classes.delete_live_class(id)
        return Response({"message": "Live class deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# styudent  class attendance
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_student_class_attendance(request):
    if request.method =="GET":
        results = student_attendance.get_attendance()
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update student attendance
@permission_classes([IsAdminUser])
@api_view(["PUT"])
def update_student_class_attendance(request, student_email):
    if request.method =="PUT":
        student_email = request.data.get("student_email")  
        course_title = request.data.get("course_title") 
        savingdata = student_attendance.update_attendance(student_email, course_title) 
        return Response({"message": "attendance updated"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#delete student attendance
@permission_classes([IsAdminUser])
@api_view(["PUT"])
def delete_student_class_attendance(request, student_email):
    if request.method =="PUT":
        student_attendance.delete_student_attendance(student_email)
        return Response({"message": "attendance deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# CRUD anouncement

@permission_classes([IsAdminUser])
@api_view(["POST"])
def create_anouncements(request):
    if request.method =="POST":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = anouncement(tutor, title, content)
        savingdata.save()
        return Response({"message": "ANOUNCEMENT CREATED"},status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# VIEW  single anouncement by id

@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_single_anouncement(request, id):
    if request.method =="GET":
        results = announcements.view_anouncement(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update anouncement

@permission_classes([IsAdminUser])
@api_view(["PUT"])
def update_anouncements(request, id):
    if request.method =="PUT":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = anouncement.update_anouncement(id, tutor, title, content)
        return Response({"message": "anouncements Updated"}status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# delete Anouncement
@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_anouncements(request, id):
    if request.method =="DELETE":
       anouncement.delete_anouncement(id)
       return Response({"message": "anouncements deleted"}status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#CRUD Assignments

@permission_classes([IsAdminUser])
@api_view(["POST"])
def create_class_assignment(request):
    if request.method =="POST":
        tutor = request.data.get("tutor")
        title = request.data.get("title")
        content = request.data.get("content")
        savingdata = assignments(tutor, title, content)
        savingdata.save()
        return Response({"message": "assignment created"}status = status.HTTP_201_CREATED)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# view assignment by id
@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_class_assignment(request, id):
    if request.method =="GET":
        results = assignments.view_assignment(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#update assignment

@permission_classes([IsAdminUser])
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


@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_class_assignment(request, id):
    if request.method =="DELETE":
        assignments.delete_assignment(id)
        return Response({"message": "assignment deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# CRUD Class timetable
@permission_classes([IsAdminUser])
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

@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_class_timetable(request, id):
    if request.method =="GET":
        results = course_timetables.view_time_table(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update time table by id
@permission_classes([IsAdminUser])
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

@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_class_timetable(request, id):
    if request.method =="DELETE":
        course_timetables.delete_timetable(id)
        return Response({"message":"time table deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

#CRUD Exam timetables


@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
@api_view(["GET"])
def view_exam_timetable(request, id):
    if request.method =="GET":
        results = exam_timetables.view_exam_time_table(id)
        return Response(results,status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST)

# update exam timetable
@permission_classes([IsAdminUser])
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

@permission_classes([IsAdminUser])
@api_view(["DELETE"])
def delete_exam_timetable(request, id):
    if request.method =="DELETE":
        exam_timetables.delete_exam_timetable(id)
        return Response({"message":"Exam timetable deleted"},status = status.HTTP_200_OK)
    return Response({"error":"Bad request"}, status = status.HTTP_400_BAD_REQUEST) 
