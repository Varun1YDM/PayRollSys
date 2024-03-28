from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('validate_password/<str:keyword>/<str:email>/',views.validate_password,name='validate_password'),
    path('clock_in/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.clock,name='clock'),
    path('attendance_data/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.attendance_data,name='attendance_data'),
    path('get_specific_data/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.get_specific_data,name='get_specific_data'),
    path('leave/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.leave,name='leave'),
    path('LeaveManagement/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.leaveManagement,name='LeaveManagement'),
    path('update_location/',views.update_location,name='update_location'),
    path('accept/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.accept,name='accept'),
    path('reject/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.reject,name='reject'),
    path('pending/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.pending,name='pending'),
    path('search/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.search,name='search'),
    path('check/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.check,name='check'),
    path('status/',views.status,name='status'),
    path('statusCheck/',views.statusCheck,name='statusCheck'),
    path('get_Status_Data/',views.get_Status_Data,name='get_Status_Data'),
    path('update_Status/',views.update_Status,name='update_Status'),
    path('get_Employee_Attendance/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.get_Employee_Attendance,name='get_Employee_Attendance'),
    path('get_Employee_Leaves/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.get_Employee_Leaves,name='get_Employee_Leaves'),
    path('leave_status/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.leave_status,name='leave_status'),
    path('festival_data/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.festival_data,name='festival_data'),
    path('org/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.org,name='org'),
    path('update/<str:Employee_id>/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.update,name='update'),
    path('leave_reject/<str:Request_id>/<str:user_name>/<str:user_type>/<str:email>/<str:user_id>',views.leave_reject,name='leave_reject'),
    path('leave_accept/<str:Request_id>/<str:user_name>/<str:user_type>/<str:email>/<str:user_id>',views.leave_accept,name='leave_accept'),
    path('submit_employee_data/<str:username>/<str:user_type>/<str:email>/<str:user_id>/<str:Request_type>',views.submit_employee_data,name='submit_employee_data'),
    path('Fest_Info/<str:username>/<str:user_type>/<str:email>/<str:user_id>',views.Fest_Info, name='Fest_Info'),
    path('Status_Info/',views.Status_Info,name='Status_Info'),

]