from rest_framework import  serializers
from .models import *
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model           = Users
        fields          = ('email','username','password')
        extra_kwargs    = {'passwords': {'write_only':True, 'required':True}}

    def create(self,validated_data):
        user            = Users.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model           = UserProfile
        fields          = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model           = Users
        fields          = (
                                "first_name","lastname","phone_number","address","city","state",
                                "district","zipcode","country","date_of_birth"
                           )