from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken
from rest_framework.request import Request
from django.contrib.auth import authenticate

from .models import *
from .serializer import *
from .utils import create_jwt_token

class UserResgistration(APIView):

    '''
        This class is used for registerign new users . 
    '''

    permission_classes = []

    def post(self,request:Request):
        user_data           = request.data
        serializer          = RegistrationSerializer(data = user_data)
        if serializer.is_valid():
            serializer.save()
            context = "Your account is created successfully, Please login to continue."
            return Response(context,status=status.HTTP_201_CREATED)
        return Response("Error in creating user account")

class UserLogin(APIView):

    '''
        This class is used to login  users to their accounts.
    '''

    permission_classes = []

    def post(self,request:Request):
        email       = request.data.get('email')
        password    = request.data.get('password')
        user        = authenticate(email=email,password=password)
        
        if user is not None:
            token       = create_jwt_token(user=user)
            context     =  ({
                "msg":"succesfull",
                "tokens":token
            })
            return Response(context,status=status.HTTP_200_OK)
        else:
            check_email = Users.objects.filter(email=email).first()
            if not check_email:
                return Response({"msg":"user with given email is not found."},status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"password is incorrect"},status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):

    '''
        This class is used to Logout users from there account.
        If in data 'all' is passed all refresh tokens for all devices will be invalid i.e;
        user will be logged out from all devices.
    '''
    
    authentication_classes = (JWTAuthentication,)
    permission_classes     = (IsAuthenticated,)

    def post(self, request):
        try:
            if self.request.data.get('all'):
                token: OutstandingToken
                for token in OutstandingToken.objects.filter(user=request.user):
                    _, _ = BlacklistedToken.objects.get_or_create(token=token)
                return Response({"status": "all refresh tokens blacklisted"})
            refresh_token = self.request.data.get('refresh')
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response({"msg": "Logged out "},status=status.HTTP_200_OK)
        except:
            return Response({"Already logged out or Server Error"},status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):

    """
        Users can create PROFILE to their choices. This will be  must in future 
        for users to maintain a profile.
        Class Allows : To create profile & View Profile.
    """

    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)

    def post(self,request):
        pass

    def get(self,request):
        pass
