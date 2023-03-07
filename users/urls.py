from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='create-user'),
    path('login/', views.UserLoginView.as_view(), name='login-user'),
    path('profile/', views.UserProfile.as_view(), name='user-profile'),
    path('logout/', views.UserLogout.as_view(), name='user-profile'),
]
