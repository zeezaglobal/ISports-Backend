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
        This class is used for registering new users . 
    '''

    permission_classes = []

    def post(self,request:Request):
        try:
            user_data           = request.data
            serializer          = RegistrationSerializer(data = user_data)
            if serializer.is_valid():
                serializer.save()
                context = "Your account is created successfully, Please login to continue."
                return Response({"msg":context},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"this is the error : {e}")
            return Response({"msg":"error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLogin(APIView):

    '''
        This class is used to login  users to their accounts.
    '''

    permission_classes = []

    def post(self,request:Request):
        try:
            email       = request.data.get('email')
            password    = request.data.get('password')
            if not (email or password):
                return Response({'msg':"email and password is must for login"},status=status.HTTP_400_BAD_REQUEST)
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
        except Exception as e:
            return Response({"msg":"error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
class UserLogout(APIView):

    '''
        This class is used to Logout users from there account.
        If in data 'all' is passed all refresh tokens for all devices will be invalid i.e;
        user will be logged out from all devices.
    '''
    
    authentication_classes = (JWTAuthentication,)
    permission_classes     = (IsAuthenticated,)

    def post(self, request,*args, **kwargs):
        try:
            if self.request.data.get('all'):
                token: OutstandingToken
                for token in OutstandingToken.objects.filter(user=request.user):
                    _, _ = BlacklistedToken.objects.get_or_create(token=token)
                return Response({"status": "all refresh tokens blacklisted"},status.HTTP_400_BAD_REQUEST)
            refresh_token = self.request.data.get('refresh')
            if not refresh_token:
                return Response({"msg": "refresh tokne is not found"},status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response({"msg": "user logged out "},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":"Already logged out or Server Error"},status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(APIView):

    """
        Users can create PROFILE to their choices. This will be  must in future 
        for users to maintain a profile.
        Class Allows : To create profile & View Profile $ Update
    """

    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)

    def post(self,request):
        '''
            Profile creation API
        '''
        try:
            user = UserProfile.objects.filter(user=request.user_id,profile_active=False)
            if user:
                profile_data = request.data
                serializer = ProfileSerializer(data = profile_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"msg": "Profile Created"},status=status.HTTP_200_OK)
                error = serializer.errors
                return Response({"errors":error},status=status.HTTP_400_BAD_REQUEST)
            context = {
                "msg":"User already have active account",
                "status":False
                }
            return Response (context,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self,request):
        '''
            Profile View API
        '''
        try :
            user_profile = UserProfile.objects.filter(user=request.user_id).first()
            if user_profile:
                serializer = ProfileSerializer(user_profile,many=False)
                context = {
                    "msg":"Profile found",
                    "data":serializer.data
                }
                return Response(context,status = status.HTTP_200_OK)
            else:
                return Response({"msg":"You don't have an profile. Please create a profile."},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request):
        '''
            Profile Updating API
        '''
        try :
            user_profile = UserProfile.objects.filter(id=request.user_id)
            if user_profile:
                serializer = ProfileSerializer(user_profile,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"msg":"Profile has been updated."})
                return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"No profile found."},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditUserDetails(APIView):

    """
        This class is used to edit the details of the user model by the user.
        AGE once set cannot be changed.

    """

    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated)

    def get(self,request):
        pass

    def put(self,request):
        pass

    def patch(self,request):
        pass

class Reset_Password(APIView):

    """
        Class for resetting the passwords for the users.
    """
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def put(self,request,*args,**kwargs):
        pass