from .mongo import db
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models



# define all the collections here
student_collection = db["student"]
users_collection = db["users"]
tutor_collection = db["tutor"]
admin_collection = db["admin"]
affiliate_collection = db["affiliate"]
affiliatewallect_collection = db["AffWallet"]
available_courses_collection = db['available_courses']
course_modules_collection = db['course_modules']
live_classes_collection = db['live_classes']
student_attendance_collection = db['student_attendance']
registered_courses_collection = db['registered_courses']
announcements_collection = db['announcements']
assignments_collection = db['assignments']
course_timetables_collection = db['course_timetables']
exam_timetables_collection = db['exam_timetables']
transactions_collection = db['transactions']
referrals_collection = db['referrals']
referral_trackers_collection = db['referral_trackers']
promoted_courses_collection = db['promoted_courses']
referal_count_collection = db["referals"]


class User:
    def __init__(self, firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.course = course
        self.address = address
        self.dob = dob
        self.phonenumber = phonenumber
        self.gender = gender
        self.created_on = datetime.now()
        self.role = role
     
# Admin

class Admin(User):
    def __init__(self, firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role=None):
        super().__init__(firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role)
        self.role = "admin"
       
    def save(self):
        admin_collection.insert_one(
            {
                "firstname":self.firstname,
                "lastname": self.lastname,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "course":self.course,
                "address": self.address,
                "dob": self.dob,
                "phonenumber":self.phonenumber,
                "gender": self.gender,
                "created_on":self.created_on,
                "role": self.role
            }
        )
    
    # get admin by id

    @staticmethod
    def get_admin(id):
        return admin_collection.find_one({
            "_id": ObjectId(id)
        })

# update admin
    @staticmethod 
    def update_admin(id, firstname, lastname, username, email, password):
        admin_collection.update_one({"_id": ObjectId(id)}, {"$set":{"firstname":firstname, "lastname":lastname,"email":email, "username":username,"password":password, "address":address, "phonenumber":phonenumber,"gender":gender, "dob":dob}})

# delete admin
    @staticmethod
    def delete_admin(id):
        admin_collection.delete_one({"_id": ObjectId(id)})
    
#get all admin
@staticmethod
def get_all_admin():
    results = admin_collection.find()
    return list(results)


# affiliate

class affiliate(User):
    def __init__(self, firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role= None):
        super().__init__(firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role)
        
        self.role = "affiliate"

    def save(self):
        affiliate_collection.insert_one(
            {
                "firstname":self.firstname,
                "lastname": self.lastname,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "course":self.course,
                "address": self.address,
                "dob": self.dob,
                "phonenumber":self.phonenumber,
                "gender": self.gender,
                "created_on":self.created_on,
                "role": self.role
            }
        )
    
    # get affiliate by id

    @staticmethod
    def get_affiliate(id):
        return affiliate_collection.find_one({
            "_id": ObjectId(id)
        })

# update affiliate
    @staticmethod 
    def update_affiliate(id, firstname, lastname, username, email, password):
        affiliate_collection.update_one({"_id": ObjectId(id)}, {"$set":{"firstname":firstname, "lastname":lastname,"email":email, "username":username,"password":password, "address":address, "phonenumber":phonenumber,"gender":gender, "dob":dob}})

# delete affiliate
    @staticmethod
    def delete_affiliate(id):
        affiliate_collection.delete_one({"_id": ObjectId(id)})
    
#get all affiliate
@staticmethod
def get_all_affiliate():
    results = affiliate_collection.find()
    return list(results)




class Student(User):
    def __init__(self, firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role =None):
        super().__init__(firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role)
        self.role= "student"

    def save(self):
        student_collection.insert_one(
            {
               "firstname":self.firstname,
                "lastname": self.lastname,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "course":self.course,
                "address": self.address,
                "dob": self.dob,
                "phonenumber":self.phonenumber,
                "gender": self.gender,
                "created_on":self.created_on,
                "role": self.role

            }
        )
    
    # get user by id

    @staticmethod
    def get_student(id):
        return student_collection.find_one({
            "_id": ObjectId(id)
        })

# update user
    @staticmethod 
    def update_student(id, firstname, lastname, username, email, password):
        student_collection.update_one({"_id": ObjectId(id)}, {"$set":{"firstname":firstname, "lastname":lastname,"email":email, "username":username,"password":password, "address":address, "phonenumber":phonenumber,"gender":gender, "dob":dob}})

# delete user
    @staticmethod
    def delete_student(id):
        student_collection.delete_one({"_id": ObjectId(id)})
    
#get all users
@staticmethod
def get_all_students():
    results = student_collection.find()
    return list(results)

class Tutor:
    def __init__(self, firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role=None):
        super().__init__(firstname, lastname, username, email, password,course,address,dob,phonenumber,gender,role)
        self.role= "tutor"

    def save(self):
        tutor_collection.insert_one(
            {
               "firstname":self.firstname,
                "lastname": self.lastname,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "course":self.course,
                "address": self.address,
                "dob": self.dob,
                "phonenumber":self.phonenumber,
                "gender": self.gender,
                "created_on":self.created_on,
                "role": self.role
            }
        )
    
    # get tutor by id

    @staticmethod
    def get_tutor(id):
        return tutor_collection.find_one({
            "_id": ObjectId(id)
        })

# update tutor
    @staticmethod 
    def update_tutor(id, firstname, lastname, username, email, password):
        tutor_collection.update_one({"_id": ObjectId(id)}, {"$set":{"firstname":firstname, "lastname":lastname,"email":email, "username":username,"password":password, "address":address, "phonenumber":phonenumber,"gender":gender, "dob":dob}})

# delete tutor
    @staticmethod
    def delete_tutor(id):
        tutor_collection.delete_one({"_id": ObjectId(id)})
    
#get all tutors
@staticmethod
def get_all_tutors():
    results = tutor_collection.find()
    return list(results)



# courses
class available_courses:
    def __init__(self, author, title, slug):
        self.author = author
        self.title = title
        self.slug = slug
    #add course
    def add_course(self):
        available_courses_collection.insert_one({
            "title":title,
            "author":author,
            "slug": slug
        })

    # update course
    
    @staticmethod
    def update_course(title):
        available_courses_collection.update_one({"title": title}, {"$set":{"title":title, "author":author,"slug":slug}})
    
    #get all courses
    @staticmethod
    def get_courses():
        results = available_courses_collection.find()
        return list(results)
    
    #delete course by title
    @staticmethod
    def delete(title):
        available_courses_collection.delete_one({"title":title})
        return "Course deleted"

#live class
class live_classes:
    def add_live_class(self, class_name, class_description, class_link):
        self.class_name = class_name
        self.class_description = class_description
        self.class_link = class_link

    # view live class details
    def view_liveclass(id):
        results = live_classes_collection.find_one({"_id":id})
        return results

#update live class details
    @staticmethod
    def update_live_class(id):
        live_classes_collection.update_one({"_id":id}, {"$set":{"class_name":class_name,"class_description":class_description, "class_link":class_link}})

#delete liveclass details
    @staticmethod
    def delete_live_class_details(id):
        live_classes_collection.delete_one({"_id":id})

# student attendance collectioon

class student_attendance:
    def attendance(self, student_email, course_title):
        self.student_email = student_email
        self.course_title = course_title
        self.entry_time = datetime.now()

    @staticmethod
    def update_attendance(student_email):
        student_attendance_collection.update_one({"student_email": student_email}, {"$set":{"student_email":student_email, "course_title":course_title}})
    
    #get all courses
    @staticmethod
    def get_attendance():
        results = student_attendance_collection.find()
        return list(results)
    
    #delete course by title
    @staticmethod
    def delete_student_attendance(student_email):
        student_attendance_collection.delete_one({"student_email":student_email})
        return "student deleted"


# create anouncements

class anouncements:
    def create_anouncement(self, tutor, title, content):
        self.tutor = tutor
        self.title = title
        self.content = content
        self.date_created = datetime.now()

    # view anouncement 
    @staticmethod
    def view_anouncement(id):
        results = announcements_collection.find_one({"_id":id})
        return results
    
    #update Anouncement
    @staticmethod
    def update_anouncement(id):
        results = announcements_collection.update_one({"_d":id},{"tutor":tutor,"title":title,"content":content})
    
    #delete anouncement
    @staticmethod
    def delete_anouncement(id):
        announcements_collection.delete_one({"_id":id})

# Create Assignment

class assignments:
    def create_assignment(self,tutor, title, content):
        self.tutor = tutor
        self.title = title
        self.content = content
        self.date_created = datetime.now()

      # view assignment
    @staticmethod
    def view_assignment(id):
        results = assignments_collection.find_one({"_id":id})
        return results
    
    #update assignment
    @staticmethod
    def update_assignment(id):
        results = assignments_collection.update_one({"_d":id},{"tutor":tutor,"title":title,"content":content})
    
    #delete assignment
    @staticmethod
    def delete_assignment(id):
       assignments_collection.delete_one({"_id":id})

# course time table

class course_timetables:
    def create_course_time_table(self,tutor,course, class_link):
        self.course = course
        self.tutor = tutor
        self.class_link = class_link
        self.date_and_time = datetime
    
    # view time table
    @staticmethod
    def view_time_table(id):
        results = course_timetables_collection.find_one({"_id":id})
        return results
    
    # update time table

    @staticmethod
    def update_time_table(id):
        course_timetables_collection.update_one({"_id":id}, {"course":course,"tutor":tutor, "class_link":class_link})   
    
    #delete timetable
    @staticmethod
    def delete_timetable(id):
        course_timetables_collection.delete_one({"_id":id})


# exam time table
class exam_timetables:
    def create_exam_time_table(self,title,course, class_link):
        self.course = course
        self.title = title
        self.class_link = class_link
        self.date_and_time = datetime
    
    # view  exam time table
    @staticmethod
    def view_exam_time_table(id):
        results = exam_timetables_collection.find_one({"_id":id})
        return results
    
    # update  exam time table

    @staticmethod
    def update_exam_time_table(id):
        exam_timetables_collection.update_one({"_id":id}, {"course":course,"title":title, "class_link":class_link})   
    
    #delete  exam timetable
    @staticmethod
    def delete_exam_timetable(id):
        exam_timetables_collection.delete_one({"_id":id})

class AffiliateWallet:
    def __init__(self, affiliate_id, balance = None, number_of_referals = None):
        self.affiliate_id = affiliate_id
        self.balance = 0
        self.date_created = datetime.now()
        self.number_of_referals = 0
        

        def save(self):
           affiliatewallect_collection.insert_one({
           "affiliate_id": self.affiliate_id,
           "balance": self.balance,
           "referalnumber": self.number_of_referals
        })

        def get_all():
            results = affiliatewallect_collection.find()
            return list(results)

        def get_by_id(affiliate_id):
            results = affiliatewallect_collection.find_one({"affiliate_id":affiliate_id})
            return (results)
        def delete_wallet(username):
            results = affiliatewallect_collection.delete_one({"username":username}) 


       

