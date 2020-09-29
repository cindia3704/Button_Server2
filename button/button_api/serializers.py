from rest_framework import serializers, fields
from .models import User, UserManager, Cloth_Specific
from django.contrib.auth.hashers import make_password


class User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'password', 'userEmail',
                  'userNickName', 'userGender', 'dateRegistered', 'confirmedEmail']

    def create(self, validated_data):
        user = User.objects.create(
            userEmail=validated_data['userEmail'],
            password=make_password(validated_data['password']),
            userGender=validated_data['userGender'],
            userNickName=validated_data['userNickName']
        )
        user.save()
        return user


class Cloth_SpecificSerializer(serializers.ModelSerializer):
    SEASON_CHOICES = (
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('FALL', 'Fall'),
        ('WINTER', 'Winter'),
        ('ETC', 'etc'),
    )
    season = serializers.MultipleChoiceField(choices=SEASON_CHOICES)

    photo = serializers.ImageField(
        use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = Cloth_Specific
        fields = ['id', 'clothID', 'color', 'season',
                  'category', 'dateBought', 'dateLastWorn', 'photo']


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.ModelSerializer):
    #token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['id', 'password', 'userEmail',
                  'userNickName']
