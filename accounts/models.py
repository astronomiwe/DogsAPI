from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

import jwt

from datetime import datetime, timedelta
from django.utils.timezone import now

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        """Создает и возвращает пользователя с имэйлом, паролем и именем."""
        if email is None:
            raise TypeError('Необходимо указать е-майл (e-mail).')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Создает и возввращет пользователя с привилегиями суперадмина."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователи"""
    id = models.AutoField
    email = models.EmailField(db_index=True, unique=True, null=False, verbose_name='регистрационный email')
    avatar = models.ImageField(verbose_name="аватар", upload_to='users/avatars', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    USERNAME_FIELD = 'email'  # как логинимся

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = "user"

    @property
    def access_token(self):
        """
        Получение токена пользователя как свойства класса - user.token, вместо user._generate_jwt_token()"""
        return self._generate_jwt_token(token_type="access_token")

    @property
    def refresh_token(self):
        """
        Получение токена пользователя как свойства класса - user.token, вместо user._generate_jwt_token()"""
        return self._generate_jwt_token(token_type="refresh_token")


    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать email.
        """
        return self.email

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.email

    def _generate_jwt_token(self, token_type):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена определяется типом токена
        """
        if token_type == "access_token":
            dt = datetime.now() + timedelta(days=5)

            access_token = jwt.encode({
                'id': self.pk,
                'email': self.email,
                'exp': dt
            }, settings.SECRET_KEY, algorithm='HS256')

            return access_token

        elif token_type == "refresh_token":
            dt = datetime.now() + timedelta(days=30)

            refresh_token = jwt.encode({
                'id': self.pk,
                'email': self.email,
                'exp': dt
            }, settings.SECRET_KEY, algorithm='HS256')

            return refresh_token
