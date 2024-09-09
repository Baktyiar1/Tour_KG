from rest_framework import serializers

from .models import MyUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'password'
        )

    def create(self, validated_data):
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value


class UserProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'email',
            'avatar',
            'age'
        )

class UserProfilUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'avatar',
            'age'
        )



