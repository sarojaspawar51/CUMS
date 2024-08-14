from django.urls import  path
from flask import views
from .views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>/', UserInfoAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/profile', UserProfileInfoAPIView.as_view(), name='user-profile'),
    # path('fetch-data/', fetch_data, name='fetch_data'), 
    path('public/', PublicAPIView.as_view()),

]

