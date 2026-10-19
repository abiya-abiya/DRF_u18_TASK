import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_access_token(user_id):#JWT access token yaratib olish
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def create_refresh_token(user_id):#JWT refresh token yaratish
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_token(token):#Kelgan JWT tokenni dekodlab o'qish
    return jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])