import re

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import connection, models

BAN_CHOICES = [
    ('SECOND', 'SECOND'),
    ('MINUTE', 'MINUTE'),
    ('HOUR', 'HOUR'),
    ('DAY', 'DAY'),
    ('WEEK', 'WEEK'),
    ('MONTH', 'MONTH'),
    ('YEAR', 'YEAR'),
    ('PERM', 'PERM'),
]


class UserManager(BaseUserManager):
    def create_user(self, login, email, social_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not login:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            social_id=social_id
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, social_id, password):
        user = self.create_user(
            login,
            email,
            social_id=social_id,
            password=password,
        )

        user.admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    login = models.CharField('Login / username', max_length=30, unique=True)
    password = models.CharField('Password', max_length=45)
    email = models.EmailField('E-mail', max_length=64, unique=True)
    social_id = models.CharField('Kod usunięcia postaci', max_length=7,
        validators=[RegexValidator(
            regex=r'^\d{7}$',
            message='Kod usunięcia postaci musi zawierać 7 cyfr',
        )]
    )

    powod = models.TextField('Powód banu', null=True, blank=True)
    banlength = models.CharField('Długość banu', max_length=30,
        choices=BAN_CHOICES, null=True, blank=True)

    coins = models.IntegerField('SM', default=0)

    admin = models.BooleanField('Admin?', default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'password', 'social_id']

    objects = UserManager()

    class Meta:
        db_table = "account"

    def get_full_name(self):
        return self.login

    def get_short_name(self):
        return self.login

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def set_password(self, raw_password):
        self.password = self._get_password(raw_password)
        self._password = raw_password

    def _get_password(self, raw_password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT PASSWORD(%s)", [raw_password])
            row = cursor.fetchone()
            return row[0]

    def check_password(self, raw_password):
        password = self._get_password(raw_password)
        return self.password == password

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return True