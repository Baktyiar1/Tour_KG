from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import MyUser


# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = MyUser
#         fields = (
#             'username',
#             'last_name',
#             'email',
#             'password'
#         )
#
#     def create(self, validated_data):
#         user = MyUser(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
    # def validate_email(self, value):
    #     if MyUser.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("Пользователь с таким email уже существует.")
    #     return value

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    email = serializers.EmailField(required=True)  # Обязательно указываем

    def custom_signup(self, request, user):
        email = self.validated_data.get('email')
        if not email:
            raise serializers.ValidationError("Email is required.")
        user.username = self.validated_data.get('username')
        user.last_name = self.validated_data.get('last_name')
        user.email = email
        user.save()


class UserProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'last_name',
            'email',
            'avatar',
            'phone_number',
            'age',
            'address'
        )

class UserProfilUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'last_name',
            'email',
            'avatar',
            'age',
            'phone_number',
            'address'
        )



