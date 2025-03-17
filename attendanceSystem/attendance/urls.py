from django.urls import path,include
from attendance import views

urlpatterns = [
    path('checkIn/', views.AttendanceCheckInView.as_view(), name='attendance-check-in'),
    path('checkOut/<int:attendance_id>/', views.AttendanceCheckOutView.as_view(), name='attendance-check-out'),
]