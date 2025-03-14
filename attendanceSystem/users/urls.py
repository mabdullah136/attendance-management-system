from django.urls import path,include
from users import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('update/', views.UserUpdateView.as_view(), name='user-update'),
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token-refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    
]