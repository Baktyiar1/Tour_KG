from rest_framework import serializers
from django.utils import timezone
from tour.service import get_client_ip
from django.db import models
from django.db.models import Avg
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import MyUser
from tour.models import Tour, Booking, Date_tour, Payment, Reviews, Payment_method

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
class TourProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = (
            'title',
            'description',
            'headline_img'
        )
class ProfilBookingSerializer(serializers.ModelSerializer):
    tour = TourProfilSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = (
            'tour',
            'total_price'
        )

class UserBookingSerializer(serializers.ModelSerializer):
    bookings = ProfilBookingSerializer(source='client_booking', many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = (
            'bookings',  # Бронирования пользователя
        )

class Date_tourIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date_tour
        fields = '__all__'

class TourListSerializer(serializers.ModelSerializer):
    date_tour = Date_tourIndexSerializer(many=True)
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = Tour
        fields = (
            'id',
            'headline_img',
            'title',
            'description',
            'participants_price',
            'price',
            'discount_price',
            'date_tour',
        )


    def get_discount_price(self, obj):
        now = timezone.now()
        if obj.discount_start_date and obj.discount_end_date:
            if obj.discount_start_date <= now <= obj.discount_end_date:
                return obj.discount_price
        return None

class AuthorUserProfilSerializer(serializers.ModelSerializer):
    tours = TourListSerializer(many=True, read_only=True)
    class Meta:
        model = MyUser
        fields = (
            'username',
            'last_name',
            'avatar',
            'description',
            'tours',
        )

class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'qr_code_img',
        )