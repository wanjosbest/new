from django.urls import path
from .import views
from newageapp.views import RegisterView,LoginView

urlpatterns =[
     # CRUD STUDENTS ENDPOINTS
     path("api/register-student/", RegisterView.as_view(), name="register_student"),
     path("api/view-all-students/", views.get_students_list, name="get_all_students"),
     path("api/delete-student/<int:id>/", views.delete_student, name="delete_student"),
     path("api/update-student/<int:id>/", views.update_student, name="update_student"),
     
     #CRUD COURSES ENDPOINTS
     path("api/create-course/", views.create_course, name="create_course"),
     path("api/view-all-courses/", views.view_courses, name="view_courses"),
     path("api/update-course/<int:id>/",views.update_course, name="update_course"),
     path("api/delete-course/<int:id>/", views.delete_course, name="delete_course"),

     # CRUD LIVE CLASS ENDPOINTS
     path("api/create-live-class/", views.create_live_class, name="create_live_class"),
     path("api/view-live-class/", views.view_live_class, name="view_live_class"),
     path("api/update-live-class/<int:id>/", views.update_live_class, name="update_live_class"),
     path("api/delete-live-class/<int:id>/", views.delete_live_class, name="delete_live_class"),
     #CRUD CLASS ATTENDANCE ENDPOINTS
     path("api/create-class-attendance/", views.student_class_attendance, name="create_student_class_attendance"),
     path("api/view-class-attendance/", views.view_student_class_attendance, name="view_student_class_attendance"),
     path("api/update-class-attendance/<student_email>/", views.update_student_class_attendance, name="update_student_class_attendance"),
     path("api/delete-class-attendance/<student_email>/", views.delete_student_class_attendance, name="delete_student_class_attendance"),
     #CRUD Anouncement ENDPOINTS
     path("api/create-anouncement/", views.create_anouncements, name="create_anouncement"),
     path("api/view-anouncement/<int:id>/", views.view_single_anouncement, name="view_anouncement"),
     path("api/update-anouncements/<int:id>/",views.update_anouncements, name="update_anouncement"),
     path("api/delete-anouncement/<int:id>/", views.delete_anouncements, name="delete_anouncement"),
     # CRUD ASSIGNMENTS ENDPOINTS
     path("api/create-class_assignment/", views.create_class_assignment, name="create_assignment"),
     path("api/view-class-assignment/<int:id>/", views.view_class_assignment, name="view_assignment"),
     path("api/update-class-assignment/<int:id>/",views.update_class_assignment, name="update_assignment"),
     path("api/delete-class-assignment/<int:id>/", views.delete_class_assignment, name="delete_assignment"),
     #CRUD CLASS TIMETABLE ENDPOINTS
     path("api/create-class-timetable/", views.create_class_timetable, name="create_class_timetable"),
     path("api/view-class-timetable/", views.view_class_timetable, name="view_class_timetable"),
     path("api/update-class-timetable/<int:id>/",views.update_class_timetable, name="update_class_timetable"),
     path("api/delete-class-timetable/<int:id>/", views.delete_class_timetable, name="delete_class_timetable"),
     #CRUD EXAM TIMETABLE ENDPOINTS
     path("api/create-exam-timetable/", views.create_exam_timetable, name="create_exam_timetable"),
     path("api/view-exam-timetable/", views.view_exam_timetable, name="view_exam_timetable"),
     path("api/update-exam-timetable/<int:id>/",views.update_exam_timetable, name="update_exam_timetable"),
     path("api/delete-exam-timetable/<int:id>/", views.delete_exam_timetable, name="delete_exam_timetable"),
     #LOGIN ENDPOINT
     path("api/login-student/", LoginView.as_view(), name="login_student"),
    
]
