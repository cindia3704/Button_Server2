from rest_framework import serializers, fields
from .models import User, UserManager, Cloth_Specific, Outfit_Specific, Friend, KNN, Calendar_Specific
from django.contrib.auth.hashers import make_password


class User_Serializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        use_url=True, max_length=None, required=False)

    class Meta:
        model = User
        fields = ['id', 'password', 'userEmail',
                  'userNickName', 'userGender', 'dateRegistered', 'confirmedEmail', 'photo']

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(required=True)
        newPassword = serializers.CharField(required=True)


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

    STYLE_CHOICES = (
        ('CASUAL', 'Casual'),
        ('SEMI-FORMAL', 'Semi-formal'),
        ('FORMAL', 'Formal'),
        ('OUTDOOR', 'Outdoor'),
        ('VACANCE', 'Vacance'),
    )
    style = serializers.MultipleChoiceField(choices=STYLE_CHOICES,
                                            required=False)
    photo = serializers.ImageField(
        use_url=True, max_length=None, required=False)

    class Meta:
        model = Cloth_Specific
        fields = ['id', 'clothID', 'season',
                  'category', 'photo', 'style', 'outfit']
        extra_kwargs = {'outfit': {'required': False}}


class OutfitSerializer(serializers.ModelSerializer):
    #outfit_clothes = Cloth_SpecificSerializer(many=True, required=False)
    clothes = Cloth_SpecificSerializer(many=True, read_only=True)

    class Meta:
        model = Outfit_Specific
        fields = ('id', 'outfitID', 'outfitName',
                  'clothes', 'count')
        extra_kwargs = {'clothes': {'required': False}}


class CalendarSerializer(serializers.ModelSerializer):
    outfit_worn = OutfitSerializer(read_only=True)
    diary = serializers.CharField(required=False)

    class Meta:
        model = Calendar_Specific
        fields = ('id', 'calendarID', 'date',
                  'outfit_worn', 'diary')
        extra_kwargs = {'outfit_worn': {'required': False}}


class Friend_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'frienduser', 'accepted', 'timestamp')


class KNN_Serializer(serializers.ModelSerializer):
    SEASON_CHOICES = (
        ('SPRING', 'SPRING'),
        ('SUMMER', 'SUMMER'),
        ('FALL', 'FALL'),
        ('WINTER', 'WINTER'),
        ('ETC', 'ETC'),
    )
    season = serializers.MultipleChoiceField(
        choices=SEASON_CHOICES, required=False)

    class Meta:
        model = KNN
        fields = ('id', 'KNNID', 'place1', 'place2', 'people1',
                  'people2', 'event1', 'event2', 'mood', 'season', 'style')

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
