from datetime import datetime
import re

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import connection, models

OK_STATUS = 'OK'
WEBBLK_STATUS = 'WEBBLK'
BLOCK_STATUS = 'BLOCK'

STATUS_CHOICES = [
    (OK_STATUS, 'Konto aktywne'),
    (WEBBLK_STATUS, 'Brak aktywacji email'),
    (BLOCK_STATUS, 'Zbanowane'),
]


class UserManager(BaseUserManager):
    def create_user(self, login, email, social_id, password=None, status=WEBBLK_STATUS):
        if not email:
            raise ValueError('Users must have an email address')

        if not login:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            social_id=social_id,
            status=status
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
            status=OK_STATUS
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
    availDt = models.DateTimeField(default=datetime(1, 1, 1))

    coins = models.IntegerField('SM', default=0)

    admin = models.BooleanField('Admin?', default=False)

    status = models.CharField('Status', max_length=8, choices=STATUS_CHOICES,
        default=WEBBLK_STATUS)

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
        return self.status == OK_STATUS
