from rest_framework import serializers

from .models import MyUser

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'phone_number',
            'password'
        )

    def create(self, validated_data):
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_phone_number(self, value):
        if MyUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
        return value


class UserProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'email',
            'phone_number',
            'avatar',
            'age'
        )

class UserProfilUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'phone_number',
            'avatar',
            'age'
        )