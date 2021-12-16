from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from jwt import decode

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Authorization'

    def _authenticate_credentials(self, request, access_token):
        """
        Попытка аутентификации с предоставленными данными. Если успешно -
        вернуть пользователя и токен, иначе - сгенерировать исключение.
        """
        try:
            payload = decode(request.headers['Authorization'],
                             settings.SECRET_KEY, algorithms='HS256')
        except Exception:
            msg = 'Ошибка аутентификации. Невозможно декодировать токен.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(id=payload['id'])
        except ObjectDoesNotExist:
            msg = 'Пользователь соответствующий данному токену не найден.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Данный пользователь деактивирован.'
            raise exceptions.AuthenticationFailed(msg)

        return user, access_token

    def authenticate(self, request):
        """
        Метод authenticate вызывается каждый раз, независимо от того, требует
        ли того эндпоинт аутентификации. 'authenticate' имеет два возможных
        возвращаемых значения:
            1) None - мы возвращаем None если не хотим аутентифицироваться.
            Обычно это означает, что мы значем, что аутентификация не удастся.
            Примером этого является, например, случай, когда токен не включен в
            заголовок.
            2) (user, access_token) - мы возвращаем комбинацию пользователь/токен
            тогда, когда аутентификация пройдена успешно. Если ни один из
            случаев не соблюден, это означает, что произошла ошибка, и мы
            ничего не возвращаем. В таком случае мы просто вызовем исключение
            AuthenticationFailed и позволим DRF сделать все остальное.
        """
        request.user = None

        byte_token = authentication.get_authorization_header(request)

        if not byte_token:
            return None

        access_token = byte_token.decode('utf-8')

        return self._authenticate_credentials(request, access_token)


def get_token_payload(request):
    """
    Возвращает payload токена
    :param request: запрос http
    :return: dict payload
    """
    return decode(request.headers['Authorization'], settings.SECRET_KEY, algorithms='HS256')


def update_tokens_if_need(request):
    payload = get_token_payload(request)
    lifetime = datetime.fromtimestamp(payload["exp"]) - datetime.now()
    if lifetime < timedelta(days=1):
        user = User.objects.get(id=payload["id"])
        # todo добавить старый токен в чс?
        return {"refresh_token": user.refresh_token,
                "access_token": user.access_token}
    else:
        return {}
