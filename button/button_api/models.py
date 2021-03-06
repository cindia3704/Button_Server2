# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, userEmail, userGender, userNickName, is_staff=False, is_admin=False, is_active=True, confirmedEmail=False, password=None):
        if not userEmail:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not userGender:
            raise ValueError("Users must have a gender")
        if not userNickName:
            raise ValueError("Users must have a nickname")
        user_obj = self.model(
            userEmail=self.normalize_email(userEmail)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.confirmedEmail = confirmedEmail
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, userEmail, userGender, userNickName, password=None):
        user = self.create_user(
            userEmail=userEmail,
            password=password,
            userGender=userGender,
            userNickName=userNickName,
            is_staff=True,
            is_admin=True,
            confirmedEmail=False,
        )
        return user


class User(AbstractBaseUser):
    userEmail = models.EmailField(
        max_length=255, unique=True, verbose_name="User Email", default='a@gmail.com')
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    confirmedEmail = models.BooleanField(default=False)
    userNickName = models.CharField(
        max_length=64, verbose_name="User Nickname", default="NickName")
    GENDER_CHOICES = (
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('ETC', 'etc'),
    )
    userGender = models.CharField(max_length=10,
                                  choices=GENDER_CHOICES,
                                  default='ETC')
    dateRegistered = models.DateTimeField(
        auto_now_add=True)
    photo = models.ImageField(
        default='button/media/default.jpg', null=True, blank=True)
    # friendlist = models.ManyToManyField(
    #     'Friend', related_name="friend_users", blank=True)
    USERNAME_FIELD = 'userEmail'
    # email & password = required by default
    REQUIRED_FIELDS = ['userGender', 'userNickName', ]
    objects = UserManager()

    def __str__(self):
        return self.userEmail

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_gender(self):
        return self.userGender

    def get_nickname(self):
        return self.userNickName

    def get_email(self):
        return self.userEmail

    def get_friends(self):
        return self.friends

    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active


# class Profile(models.Model):
#     user = models.OneToOneField(User)
# class Date(models.Model):
#     date = models.DateField(default=datetime.date.today())


class Cloth_Specific(models.Model):
    id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    clothID = models.AutoField(primary_key=True,
                               verbose_name="closetID",
                               unique=True)
    SEASON_CHOICES = (
        ('HWAN', 'HWAN'),
        ('SUMMER', 'SUMMER'),
        ('WINTER', 'WINTER'),
        ('ETC', 'ETC'),
    )
    season = MultiSelectField(choices=SEASON_CHOICES, default='ETC')
    CATEGORY_CHOICES = (
        ('TOP', 'Top'),
        ('BOTTOM', 'Bottom'),
        ('DRESS', 'Dress'),
        ('OUTER', 'Outer'),
        ('ETC', 'etc'),
    )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10,
                                default='ETC')

    STYLE_CHOICES = (
        ('CASUAL', 'Casual'),
        ('SEMI-FORMAL', 'Semi-formal'),
        ('FORMAL', 'Formal'),
        ('OUTDOOR', 'Outdoor'),
        ('VACANCE', 'Vacance'),
    )
    style = MultiSelectField(choices=STYLE_CHOICES,
                             default='CASUAL')
    photo = models.ImageField(
        default='button/media/default.jpg', null=True, blank=True)
    # dateBought = models.DateField(
    #     verbose_name='date Bought', null=True, blank=True)

    # dateLastWorn = models.DateField(
    #     verbose_name='date Last Worn', null=True, blank=True)
    # default=datetime.date.today(),
    # datesWorn = models.ManyToManyField(
    #     'Date', verbose_name='cloth dates worn', blank=True)
    outfit = models.ManyToManyField(
        'Outfit_Specific', related_name="clothes", blank=True)
    # clothes = models.ManyToManyField(
    # 'Clothes', related_name='outfit', blank=True)
    # outfit = models.ForeignKey(to=Outfit_Specific, verbose_name="outfit",
    #                            related_name="outfit_clothes", on_delete=models.PROTECT, null=True, blank=True)

    def get_outfit(self):
        return self.outfit

    def get_season(self):
        return self.season

    def get_style(self):
        return self.style

    def get_category(self):
        return self.category

    def get_photo(self):
        return self.photo

    # def get_dates(self):
    #     return self.dates


class Outfit_Specific(models.Model):
    id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", related_name="user_outfit")
    outfitID = models.AutoField(primary_key=True,
                                verbose_name="outfitID",
                                unique=True)
    outfitName = models.CharField(
        max_length=64, verbose_name="outfit name", default='NONE')
    count = models.IntegerField(
        verbose_name="입은 횟수", default=0)
    outfitBy = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Outfit_by", related_name="outfit_by", null=True)
    # dates_worn = models.ManyToManyField(
    #     'Calendar_Specific', related_name="outfit_worn", blank=True)
    # dates_outfit_worn = models.ManyToOneRel(
    #     'Date', verbose_name='dates worn', blank=True)
    # clothes = models.ManyToManyField(
    #     'Cloth_Specific', related_name="outfit", blank=True)

    def get_count(self):
        return self.count

    def get_outfitby(self):
        return self.outfitBy

    def get_owner(self):
        return self.id


class Calendar_Specific(models.Model):
    id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    calendarID = models.AutoField(primary_key=True,
                                  verbose_name="outfitID",
                                  unique=True)
    date = models.DateField(
        verbose_name='date Last Worn', default=datetime.date.today(), null=True)

    diary = models.TextField(verbose_name='diary',
                             max_length=500, null=True, blank=True)
    outfit_worn = models.ForeignKey(
        Outfit_Specific, on_delete=models.CASCADE, verbose_name="Outfit", null=True)

    def get_date(self):
        return self.date


class KNN(models.Model):
    id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User1")
    KNNID = models.AutoField(primary_key=True,
                             verbose_name="knn ID",
                             unique=True)
    SEASON_CHOICES = (
        ('HWAN', 'HWAN'),
        ('SUMMER', 'SUMMER'),
        ('WINTER', 'WINTER'),
        ('ETC', 'ETC'),
    )
    season = models.CharField(verbose_name='season', choices=SEASON_CHOICES, max_length=10,
                              default='ETC')
    place1 = models.IntegerField(default=1, verbose_name="place 1")
    place2 = models.IntegerField(default=0, verbose_name="place 2")
    people1 = models.IntegerField(default=1, verbose_name="meeting 1")
    people2 = models.IntegerField(default=0, verbose_name="meeting 2")
    event1 = models.IntegerField(default=1, verbose_name="event 1")
    event2 = models.IntegerField(default=0, verbose_name="event 2")
    mood = models.IntegerField(default=1, verbose_name="mood")
    style = models.CharField(max_length=64, verbose_name="style", null=True)

    def set_style(self, styleName):
        style = styleName

    def get_style(self):
        return self.style


class Friend(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=True)
    frienduser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_user", null=True)
    accepted = models.BooleanField(default=False)
    # timestamp = models.DateTimeField(
    #     auto_created=True, default=datetime.date.today())

    # @classmethod
    # def make_friend(cls, current_user, new_friend):
    #     friend, created = cls.objects.get_or_create(
    #         current_user=current_user
    #     )
    #     friend.users.add(new_friend)

    # @classmethod
    # def lose_friend(cls, current_user, new_friend):
    #     friend, created = cls.objects.get_or_create(
    #         current_user=current_user
    #     )
    #     friend.users.remove(new_friend)


@ receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# @receiver(reset_password_token_created)
# def password_reset_token_created(instance, reset_password_token, sender=settings.AUTH_USER_MODEL, * args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(
#         reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.userEmail]
#     )

# class CalendarOutfit(models.Model):
#     owner = odels.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")


# class Outfit(models.Model):
#     owner = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name="User")
