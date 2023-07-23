from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import date
from django.utils.translation import gettext_lazy as _

from .constants import DISTRICT_CHOICES

class UserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self,email,username,password):
        
        if not email:
            raise ValueError("Users must have an valid email address.")
        if not username :
            raise ValueError("User must have unique username.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save()
        return user 
    

    def create_superuser(self,email,username,password):
        user    =  self.create_user(
                                    email = self.normalize_email(email),
                                    username = username,
                                    password = password,
                            )
        
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        user.save()
        return user
    
class Users(AbstractBaseUser,PermissionsMixin):

    email           = models.EmailField(_('email'), unique = True)
    first_name      = models.CharField(_('first_name'), max_length = 100, blank = True)
    last_name       = models.CharField(_('last_name'), max_length = 100, blank = True)
    username        = models.CharField(_('nickname'), max_length = 100, unique= True)
    phone_number    = models.CharField(max_length=30, blank=True, null=True)
    address         = models.CharField(_('user address'), max_length=500, blank=True)
    city            = models.CharField(_('user city'), max_length=250, blank=True)
    state           = models.CharField(_('user state'), max_length=250, blank=True)
    district        = models.CharField(max_length=2,choices= DISTRICT_CHOICES,null=True,blank=True)
    zipcode         = models.CharField(_('user zipcode'), max_length=250, blank=True)
    country         = models.CharField(_('user country'), max_length=250, blank=True)
    created_on      = models.DateTimeField(_('user created on'), auto_now_add=True)
    updated_on      = models.DateTimeField(_('user updated on'), auto_now=True)

    objects = UserManager()
    
    
    

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['username']
    
    def has_perm(self,perm,obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
    class Meta:
        verbose_name_plural = "Users"
    

