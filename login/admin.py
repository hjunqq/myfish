from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.


admin.site.empty_value_display = '(None)'

class UserLogInfoList(admin.ModelAdmin):
    list_display = ('pk','user','logInIP','logInTime','logOutTime','UserAgent')


    
    

admin.site.register(UserLogInfo,UserLogInfoList)
