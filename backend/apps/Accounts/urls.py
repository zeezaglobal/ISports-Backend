from django.urls import path
from .api import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

'''
    HERE THIS CONTAINS ALL THE URLs REQUIRED FOR :
            
    [
        Registrration
        Login
        Logout
        Refresh Token
        Profile Creation For Users
        Updation of Profile
        Resetting User password
        Editng user account settings
    ]
        
'''


urlpatterns = [

    path('register/',UserResgistration.as_view(),name = "registration"),
    path('login/',UserLogin.as_view(),name='login'),
    path('refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('profile/',UserProfileViewSet.as_view(),name="user_profile"),
    


]