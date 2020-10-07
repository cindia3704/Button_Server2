# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Cloth_Specific, Outfit_Specific, Friend, KNN
from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
User = get_user_model()

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('userEmail', 'userGender', 'admin')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('userEmail', 'password')}),
        ('Personal info', {
         'fields': ('userNickName', 'userGender',)}),
        ('Permissions', {'fields': ('admin', 'active', 'confirmedEmail',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userEmail', 'password1', 'password2', 'userGender', 'userNickName',)}
         ),
    )
    search_fields = ('userEmail',)
    ordering = ('userEmail',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.register(Friend)

admin.site.register(Cloth_Specific)

admin.site.register(Outfit_Specific)
admin.site.register(KNN)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
