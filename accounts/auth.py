import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import CustomUser


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            # 'Bearer <token>' ni ikkiga ajratamiz
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            # Tokenni SECRET_KEY orqali dekod qilamiz
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)

            # DRF ga (user, auth) ko'rinishida foydalanuvchini topshiramiz
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token muddati tugagan")
        except (jwt.DecodeError, CustomUser.DoesNotExist):
            raise AuthenticationFailed("Yaroqsiz token")