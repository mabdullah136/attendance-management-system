from django.urls import path,include
from holiday import views

urlpatterns = [
    path('create/', views.HolidayCreateView.as_view(), name='holiday-create'),
    path('list/', views.HolidayListView.as_view(), name='holiday-list'),
    
]