from django.urls import path,include
from attendance import views

urlpatterns = [
    path('create/', views.AttendanceCreateView.as_view(), name='attendance-create'),
]