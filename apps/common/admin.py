from models import *
from django.contrib import admin
from django.contrib.contenttypes import generic

class PhotoAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Photo,PhotoAdmin)
#admin.site.register(UserProfile,UserProfileAdmin)
