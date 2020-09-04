from rest_framework import serializers, fields
from .models import User, UserManager, Cloth_Specific


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'userEmail',
                  'userNickName', 'userGender', 'dateRegistered', 'confirmedEmail']


class User_findEmail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userEmail']


class Cloth_SpecificSerializer(serializers.ModelSerializer):

    SEASON_CHOICES = (
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('FALL', 'Fall'),
        ('WINTER', 'Winter'),
        ('ETC', 'etc'),
    )
    season = serializers.MultipleChoiceField(choices=SEASON_CHOICES)

    class Meta:
        model = Cloth_Specific

        fields = ['id', 'clothID', 'color', 'season',
                  'category', 'dateBought', 'dateLastWorn']
