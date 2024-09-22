from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone

User = get_user_model()


class TourAuthorRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    social_links = models.JSONField(default=dict, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def approve_author(self):
        self.is_approved = True
        self.user.is_author = True
        self.user.save()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.description[:20]}"

    class Meta:
        verbose_name = "Заявка автора"
        verbose_name_plural = "Заявки авторов"


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banner_img')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class Image(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название', blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='image/', verbose_name='Изорожение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
class Region(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField('Описание')

    image = models.ImageField(upload_to='region_img/')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Date_tour(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"
    class Meta:
        verbose_name = "Дата тура"
        verbose_name_plural = "Даты туров"


class Tour(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tours')
    headline_img = models.ImageField(upload_to='headline_img/')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField('Описание')
    duration = models.CharField(
        max_length=50,
        verbose_name='Продолжительность'
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')
    discount_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена в скидке', blank=True, null=True)
    discount_start_date = models.DateTimeField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)
    participants_price = models.CharField(
        max_length=20,
        choices=(
            ('за одного', 'за одного'),
            ('за группу', 'за группу'),
        ),
        default='за одного'
    )
    max_participants = models.PositiveSmallIntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='tours')
    regions = models.ManyToManyField(Region, related_name='tours')
    date_tour = models.ManyToManyField(Date_tour, related_name='tours')
    images = models.ManyToManyField(Image, related_name='tours')

    is_active = models.BooleanField(
        'Активность',
        default=True
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def clean(self):
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError("Цена со скидкой не может быть больше первоначальной цены.")
        if self.discount_price and (not self.discount_start_date or not self.discount_end_date):
            raise ValidationError("Для скидки необходимо указать дату начала и окончания.")
        if self.discount_start_date and self.discount_end_date and self.discount_start_date >= self.discount_end_date:
            raise ValidationError("Дата начала скидки не может быть позднее даты окончания.")

    def get_current_price(self):
        """Возвращает актуальную цену с учётом скидки."""
        now = timezone.now()
        if self.discount_price and self.discount_start_date <= now <= self.discount_end_date:
            return self.discount_price
        return self.price

    def get_total_booked_participants(self):
        """Возвращает общее количество забронированных участников."""
        return Booking.objects.filter(tour=self).aggregate(total_participants=Sum('participants'))['total_participants'] or 0

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_booking')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_booking')
    comments = models.TextField()
    date_tour = models.ForeignKey(Date_tour, on_delete=models.PROTECT)
    participants = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    language = models.PositiveSmallIntegerField(
        choices=(
            (1, 'English'),
            (2, 'Русский'),
            (3, 'Кыргыз')
        ),
        default=2
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Ожидает подтверждения'),
            (2, 'Подтвержден'),
            (3, 'Отказ')
        ),
        default=1
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Валидация количества участников
        if self.participants < 1:
            raise ValidationError("Количество участников должно быть хотя бы 1.")
        if self.participants > self.tour.max_participants:
            raise ValidationError(f"Максимальное количество участников для этого тура: {self.tour.max_participants}.")

    def __str__(self):
        return f"Бронирование по {self.client.username} для {self.tour.title}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ('client', 'tour', 'date_tour')

class Payment_method(models.Model):
    payment_name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.payment_name

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.ForeignKey(Payment_method, on_delete=models.PROTECT)

    status = models.PositiveSmallIntegerField(
        choices=[
            (1, 'Платеж ожидает обработки'),
            (2, 'Платеж успешно завершён'),
            (3, 'Произошла ошибка, и платеж не завершён'),
        ],
        default=1
    )
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Оплата за бронирование {self.booking.id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"



class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=45)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="тур", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.tour}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )
    tour = models.ForeignKey(Tour, verbose_name="тур", on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.name} - {self.tour}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    tours = models.ManyToManyField(Tour, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Список желаний от {self.user.username}'

    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'


class TourView(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField("IP адрес", max_length=45, null=True, blank=True)  # Для анонимных пользователей
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username if self.user else "Аноним"} посмотрел {self.tour.title}'

    class Meta:
        verbose_name = 'Просмотр тура'
        verbose_name_plural = 'Просмотры туров'




