from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone
from .config import *


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def validate_lname(last_name):
    if len(last_name) <= MIN_LN_LEN:
        raise ValidationError(f'{last_name} is too short')


def get_positive(volume: int):
    if volume <= 0:
        raise ValidationError(f'Volume {volume} is less or equal zero')


def get_datetime():
    return datetime.now(timezone.utc)


class Categories(UUIDMixin, models.Model):
    name = models.CharField(max_length=50)
    supercategory = models.ForeignKey(
        'self', models.PROTECT, db_column='supercategory', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Категории'
        db_table = 'categories'


class Discounts(UUIDMixin, models.Model):
    date_of_creation = models.DateTimeField()
    finished = models.DateTimeField()
    product = models.ForeignKey(
        'Products', models.CASCADE, blank=True, null=True)  
    percentage = models.IntegerField(validators=(get_positive,))

    def __str__(self) -> str:
        return f'{self.product} {self.percentage}'

    class Meta:
        verbose_name_plural = "Скидки"
        db_table = 'discounts'


class Orders(UUIDMixin, models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUSES)
    user = models.ForeignKey('Users', models.SET_NULL,
                             blank=True, null=True)  
    def __str__(self) -> str:
        return f'{self.user} --- {self.status} --- {self.date.year}.{self.date.month}.{self.date.day}'

    class Meta:
        verbose_name_plural = "Заказы"
        db_table = 'orders'


class Products(UUIDMixin, models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(
        Categories, models.PROTECT, blank=True, null=True)
    weight = models.FloatField(
        blank=True, null=True, validators=[get_positive])
    description = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)
    storage_conditions = models.CharField(blank=True, null=True, max_length=45)
    number = models.IntegerField(validators=[get_positive])
    price = models.DecimalField(
        max_digits=10, decimal_places=1, validators=[get_positive])
    status = models.CharField(max_length=70, choices=PR_STATUS)
    image = models.ImageField(upload_to='photos/%Y/', null=True)

    def __str__(self) -> str:
        return f'{self.name} --- {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'products'


class OrdersToProducts(models.Model):
    product = models.ForeignKey(
        'Products', models.PROTECT, blank=True, null=True, verbose_name='Продукт')
    number = models.IntegerField(validators=(get_positive,))
    order = models.ForeignKey(Orders, models.CASCADE,
                              blank=True, null=True)  

    class Meta:

        verbose_name = 'Компонент'
        db_table = 'orders_to_products'
        unique_together = (('order', 'product'),)


class Reviews(UUIDMixin, models.Model):
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    comment = models.TextField()
    product = models.ForeignKey(Products, models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user} comment {self.product}'

    class Meta:
        verbose_name_plural = "Комментарии"
        db_table = 'reviews'


class UserAddresses(UUIDMixin, models.Model):
    name = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Адреса пользователей'
        db_table = 'user_addresses'


class UserToAddress(models.Model):
    user = models.ForeignKey('Users', models.CASCADE)
    address = models.ForeignKey(
        UserAddresses, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'user_to_address'
        unique_together = (('user', 'address'),)


class Users(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'surname', 'last_name']
    username = models.CharField(max_length=20, unique=True, null=True)
    USERNAME_FIELD = 'username'
    last_login = models.CharField(max_length=40, default='')
    is_superuser = models.BooleanField(default=False)
    email = models.CharField(max_length=40, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=get_datetime)
    EMAIL_FIELD = 'email'
    first_name = models.CharField(max_length=40, help_text="First name")
    surname = models.CharField(
        blank=True, null=True, max_length=40, help_text="Surname if you have")
    last_name = models.CharField(max_length=40, validators=[
                                 validate_lname], help_text="Last name")
    addresses = models.ManyToManyField(UserAddresses, through=UserToAddress)

    def __str__(self) -> str:
        if self.surname:
            return f'{self.first_name} {self.surname} {self.last_name}' if not self.is_superuser else 'Admin'
        return f'{self.first_name} {self.last_name}' if not self.is_superuser else 'Admin'

    def display_addresses(self):
        return '; '.join([address.name for address in self.addresses.all()])
    display_addresses.short_description = 'Addresses'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
