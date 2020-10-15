from rest_framework import serializers, fields
from .models import User, UserManager, Cloth_Specific, Outfit_Specific, Friend, KNN
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


class User_Serializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userEmail', 'confirmedEmail']


class Cloth_SpecificSerializer(serializers.ModelSerializer):
    SEASON_CHOICES = (
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('FALL', 'Fall'),
        ('WINTER', 'Winter'),
        ('ETC', 'etc'),
    )
    season = serializers.MultipleChoiceField(
        choices=SEASON_CHOICES, required=False)

    photo = serializers.ImageField(
        use_url=True, max_length=None, required=False)

    class Meta:
        model = Cloth_Specific
        fields = ['id', 'clothID', 'season',
                  'category', 'dateBought', 'dateLastWorn', 'photo', 'outfit']
        extra_kwargs = {'outfit': {'required': False}}


class OutfitSerializer(serializers.ModelSerializer):
    #outfit_clothes = Cloth_SpecificSerializer(many=True, required=False)
    clothes = Cloth_SpecificSerializer(many=True, read_only=True)

    class Meta:
        model = Outfit_Specific
        fields = ('id', 'outfitID', 'outfitName',
                  'clothes')
        extra_kwargs = {'clothes': {'required': False}}


class Friend_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'frienduser', 'accepted', 'timestamp')


class KNN_Serializer(serializers.ModelSerializer):
    class Meta:
        model = KNN
        fields = ('id', 'KNNID', 'place1', 'place2', 'meeting1',
                  'meeting2', 'event1', 'event2', 'mood', 'style')

# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


# class Friend_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friend
#         fields = ('to_user', 'from_user', 'timestamp')
#         extra_kwargs = {'to_user': {'required': False},
#                         'from_user': {'required': False}}


class ChangePasswordSerializer(serializers.ModelSerializer):
    #token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['id', 'password', 'userEmail',
                  'userNickName']
