from django.contrib import admin
from django.urls import path
from user import views
from django.views.generic import TemplateView
urlpatterns = [
    path("", views.index,name='home'),
    path("about", views.about,name='about'),
    path("contact", views.contact,name='contact'),
    path("teacher", views.teacher,name='teacher'),
    path("student", views.student,name='student'),
    path("loginteacher",views.loginteacher,name='loginteacher'),
    path("loginstudent",views.loginstudent,name="loginstudent"),
    path('teacher_dashboard',views.teacher_dashboard,name='teacher_dashboard'),
    path('student_dashboard',views.student_dashboard,name='student_dashboard'),
    

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_success/', TemplateView.as_view(template_name="password_reset_success.html"), name='password_reset_success'),
    path('mark1',views.mark1,name='mark1'),
    path('mark2',views.mark2,name='mark2'),
    path('attendance1',views.attendance1,name='attendance1'),
    path('attendance2',views.attendance2,name='attendance2'),
    path('notice1',views.notice1,name='notice1'),
    path('notice_all',views.notice_all,name='notice_all'),
    path('notice_selected',views.notice_selected,name='notice_selected'),
    path('student_marks',views.student_marks,name='student_marks'),
    path('student_attendance',views.student_attendance,name='student_attendance'),
    path('subject_detail',views.subject_detail,name='subject_detail'),
    path('payment2',views.payment2,name='payment2'),

    path('forgot_passwordS/', views.forgot_passwordS, name='forgot_passwordS'),
    path('verify_otpS/', views.verify_otpS, name='verify_otpS'),
    path('reset_passwordS/', views.reset_passwordS, name='reset_passwordS'),
  


]