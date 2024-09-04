from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        if not phone_number:
            raise ValueError('Пользователи должны иметь номер телефона')

        user = self.model(
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None):

        user = self.create_user(
            phone_number=phone_number,
            username=username
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(
        'Имя',
        max_length=123
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=17,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        blank=True,
        null=True
    )
    age = models.PositiveSmallIntegerField(
        'Возраст',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='avatar_img/',
        blank=True,
        null=True
    )

    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер'),
            (3, 'Консультант'),
            (4, 'Автор тура'),
        ),
        default=1,
        verbose_name='Статус пользователя'
    )
    is_admin = models.BooleanField(
        'Администратор',
        default=False
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



