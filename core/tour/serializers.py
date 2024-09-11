from django.db.models import Sum
from django.utils import timezone

from rest_framework import serializers

from core import settings
from .models import Tour, Region, Rating, Banner, Date_tour, User, Category, TourAuthorRequest, Booking


class BannerIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class RegionIndexSerializer(serializers.ModelSerializer):
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'title', 'image', 'total_count')

    def get_total_count(self, obj):
        return obj.tours.count()  # Подсчёт количества туров

class Date_tourIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date_tour
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')

class TourListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()
    date_tour = Date_tourIndexSerializer(many=True)
    author = AutorSerializer()
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
            'author',
            'rating_user',
            'middle_star',
            'date_tour',
        )

    def get_discount_price(self, obj):
        now = timezone.now()
        if obj.discount_start_date and obj.discount_end_date:
            if obj.discount_start_date <= now <= obj.discount_end_date:
                return obj.discount_price
        return None
class CreateRetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'tour')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            tour=validated_data.get('tour', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'title',
            'image',
            'description'
        )



class CreateTourSerializer(serializers.ModelSerializer):
    date_tour = Date_tourIndexSerializer(many=True)
    regions = RegionCreateSerializer(many=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Tour
        fields = (
            'title',
            'description',
            'headline_img',
            'duration',
            'price',
            'discount_price',
            'discount_start_date',
            'discount_end_date',
            'participants_price',
            'max_participants',
            'categories',
            'regions',
            'date_tour',
            'created_date'
        )

class BookingSerializer(serializers.ModelSerializer):
    tour = TourListSerializer()
    date_tour = Date_tourIndexSerializer(many=True)
    class Meta:
        model = Booking
        fields = (
            'id',
            'tour',
            'participants',
            'total_price',
            'date_tour',
        )













class UserAutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class TourAuthorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAuthorRequest
        fields = (
            'id',
            'description',
            'social_links'
        )

class AuthorRequestListSerializer(serializers.ModelSerializer):
    user = UserAutherSerializer()
    class Meta:
        model = TourAuthorRequest
        fields = (
            'id',
            'user'
        )


class TourAuthorRequestStatusSerializer(serializers.ModelSerializer):
    user = UserAutherSerializer()
    class Meta:
        model = TourAuthorRequest
        fields = (
            'is_approved',
        )

class AuthorRequestStatusListSerializer(serializers.ModelSerializer):
    user = UserAutherSerializer()
    class Meta:
        model = TourAuthorRequest
        fields = (
            'id',
            'user',
            'is_approved'
        )

 # на разработке
class AuthorUserProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'age',)



