# Generated by Django 5.1.1 on 2024-10-07 08:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='banner_img')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Date_tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Дата тура',
                'verbose_name_plural': 'Даты туров',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=123, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='image/', verbose_name='Изорожение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Payment_method',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_name', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('participants', models.PositiveSmallIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=15)),
                ('language', models.PositiveSmallIntegerField(choices=[(1, 'English'), (2, 'Русский'), (3, 'Кыргыз')], default=2)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Ожидает подтверждения'), (2, 'Подтвержден'), (3, 'Отказ')], default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_booking', to=settings.AUTH_USER_MODEL)),
                ('date_tour', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tour.date_tour')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Платеж ожидает обработки'), (2, 'Платеж успешно завершён'), (3, 'Произошла ошибка, и платеж не завершён')], default=1)),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='tour.booking')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tour.payment_method')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='region_img/')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='tour.region')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline_img', models.ImageField(upload_to='headline_img/')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('duration', models.CharField(max_length=50, verbose_name='Продолжительность')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Цена в скидке')),
                ('discount_start_date', models.DateTimeField(blank=True, null=True)),
                ('discount_end_date', models.DateTimeField(blank=True, null=True)),
                ('participants_price', models.CharField(choices=[('за одного', 'за одного'), ('за группу', 'за группу')], default='за одного', max_length=20)),
                ('max_participants', models.PositiveSmallIntegerField(default=1)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='tours', to='tour.category')),
                ('date_tour', models.ManyToManyField(related_name='tours', to='tour.date_tour')),
                ('images', models.ManyToManyField(related_name='tours', to='tour.image')),
                ('regions', models.ManyToManyField(related_name='tours', to='tour.region')),
            ],
            options={
                'verbose_name': 'Тур',
                'verbose_name_plural': 'Туры',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='tour.reviews', verbose_name='Родитель')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='tour.tour', verbose_name='тур')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=45, verbose_name='IP адрес')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tour.ratingstar', verbose_name='звезда')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tour.tour', verbose_name='тур')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_booking', to='tour.tour'),
        ),
        migrations.CreateModel(
            name='TourAuthorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('social_links', models.JSONField(blank=True, default=dict, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка автора',
                'verbose_name_plural': 'Заявки авторов',
            },
        ),
        migrations.CreateModel(
            name='TourView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=45, null=True, verbose_name='IP адрес')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='tour.tour')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Просмотр тура',
                'verbose_name_plural': 'Просмотры туров',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tours', models.ManyToManyField(related_name='wishlisted_by', to='tour.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Список желаний',
                'verbose_name_plural': 'Списки желаний',
            },
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('client', 'tour', 'date_tour')},
        ),
    ]
