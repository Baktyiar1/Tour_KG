from django.utils import timezone
from .service import get_client_ip
from rest_framework import serializers
from .undesirable import replace_undesirable_words
from .models import (
    Tour, Region, Rating, Banner, Date_tour, User, Category, TourAuthorRequest, Booking, Wishlist,
    Payment, Image, Reviews, Payment_method
)

from django.db.models import Avg, Count
from collections import defaultdict
from rest_framework.exceptions import ValidationError

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
        fields = ('star', 'tour')  # Убедитесь, что 'ip' здесь нет

    def create(self, validated_data):
        ip = get_client_ip(self.context['request'])  # Получаем IP пользователя
        # Создаем новый объект Rating с уникальным IP
        return Rating.objects.create(ip=ip, **validated_data)

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


class DateTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date_tour
        fields = '__all__'

# бронирования

class BookingTourSerializer(serializers.ModelSerializer):
    author = AutorSerializer(read_only=True)
    class Meta:
        model = Tour
        fields = (
            'title',
            'price',
            'discount_price',
            'headline_img',
            'author'
        )

        read_only_fields = ('title', 'price', 'discount_price', 'headline_img', 'author')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number'
        )

        read_only_fields = ('email', 'username', 'phone_number')


class BookingSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # Теперь клиент редактируемый
    tour = BookingTourSerializer(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), source='tour', write_only=True)
    participants = serializers.IntegerField(default=1)

    class Meta:
        model = Booking
        fields = (
            'id',
            'client',
            'tour',
            'tour_id',  # Это поле будет использоваться для передачи ID тура
            'participants',
            'comments',
            'language',
            'total_price',
            'date_tour',
            'status',
            'created_date'
        )
        read_only_fields = ('status', 'total_price', 'created_date', 'client')

    def validate(self, data):
        request = self.context.get('request')
        client = request.user

        if client.is_anonymous:
            raise serializers.ValidationError("Пользователь не авторизован.")

        tour = data.get('tour')
        date_tour = data.get('date_tour')

        if Booking.objects.filter(client=client, tour=tour, date_tour=date_tour).exists():
            raise serializers.ValidationError("Такое бронирование уже существует для этой даты.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        client = request.user
        tour = validated_data['tour']
        participants = validated_data.get('participants', 1)

        total_booked = tour.get_total_booked_participants()
        if participants + total_booked > tour.max_participants:
            raise serializers.ValidationError(
                f"Максимальное количество участников для этого тура: {tour.max_participants}."
                f" Текущее количество забронированных участников: {total_booked}"
            )

        # Логика расчета цены
        if tour.participants_price == 'за одного':
            total_price = tour.get_current_price() * participants
        else:
            total_price = tour.get_current_price()

        booking = Booking.objects.create(
            client=client,
            tour=tour,
            date_tour=validated_data['date_tour'],
            participants=participants,
            total_price=total_price
        )

        return booking


# оплата
class AutorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('qr_code_img',)
class Payment_methodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_method
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    author = AutorPaymentSerializer(read_only=True)  # Автор будет отображаться через этот сериализатор

    class Meta:
        model = Payment
        fields = (
            'booking',
            'author',
            'amount',
            'payment_method'
        )
        read_only_fields = ('amount', 'author')  # 'author' теперь тоже поле для чтения

    def create(self, validated_data):
        booking = validated_data['booking']
        amount = booking.total_price

        # Получаем автора тура через бронирование
        author = booking.tour.author

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=validated_data['payment_method']
        )

        # Привязываем автора к платежу
        payment.author = author
        payment.save()

        return payment


# заявка на авторство
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




# список желаний
class TourWishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tour
        fields = (
            'id',
            'headline_img',
            'description',
            'price',
            'discount_price',
            'title',
        )

class WishlistSerializer(serializers.ModelSerializer):
    tours = TourWishlistSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['tours', 'created_at']




# детальная страница

class FilterReviewsSerializer(serializers.ListSerializer):
    # фильтер комментариев, только parents
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.Serializer):
    # Вывод рекурсии для children
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ReviewsCreateSerializer(serializers.ModelSerializer):
    # добавление отзыва
    class Meta:
        model = Reviews
        fields = (
            'tour',
            'parent',
            'text',
        )

    def create(self, validated_data):
        request = self.context['request']
        validated_data['name'] = request.user.username

        return super().create(validated_data)

    def validate(self, data):
        text = data.get('text', '')
        cleaned_text = replace_undesirable_words(text)
        data['text'] = cleaned_text

        return data

class ReviewsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewsSerializer
        model = Reviews
        fields = ('text', 'name', 'children')

class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class RegionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'title')

class TourDetailSerializer(serializers.ModelSerializer):
    total_count = serializers.SerializerMethodField()
    total_star = serializers.SerializerMethodField()

    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()
    date_tour = Date_tourIndexSerializer(many=True)
    author = AutorSerializer()
    discount_price = serializers.SerializerMethodField()
    images = ImageDetailSerializer(many=True)
    regions = RegionDetailSerializer(many=True)
    categories = CategoryDetailSerializer(many=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Tour
        fields = (
            'author',
            'headline_img',
            'title',
            'description',
            'duration',
            'price',
            'discount_price',
            'participants_price',
            'max_participants',
            'categories',
            'regions',
            'rating_user',
            'middle_star',
            'date_tour',
            'images',
            'reviews',
            'total_count',
            'total_star'
        )

    def get_discount_price(self, obj):
        now = timezone.now()
        if obj.discount_start_date and obj.discount_end_date:
            if obj.discount_start_date <= now <= obj.discount_end_date:
                return obj.discount_price
        return None

    def get_total_count(self, obj):
        return obj.reviews.count()

    def get_total_star(self, obj):
        result = defaultdict(int)

        star_counts = obj.ratings.values('star__value').annotate(count=Count('star'))

        for star in star_counts:
            result[star['star__value']] += star['count']

        return [
            {'star': star, 'count': result[star]} for star in range(5, 0, -1)
        ]


class TourDetailCreateSerializer(serializers.ModelSerializer):

    regions = RegionDetailSerializer(many=True)
    images = ImageDetailSerializer(many=True)
    class Meta:
        model = Tour
        fields = (
            'headline_img',
            'title',
            'description',
            'duration',
            'price',
            'discount_price',
            'discount_start_date',
            'discount_end_date',
            'participants_price',
            'max_participants',
            'regions',
            'date_tour',
            'images',
        )


