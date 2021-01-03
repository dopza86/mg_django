import jwt
from django.conf import settings
from rest_framework import authentication

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            print(token)
            if token is None:
                return None
            # xjwt, jwt_token = token.split(" ")
            decoded = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'],
                                 options={"verify_exp": False})

            pk = decoded.get("user_id")
            print(decoded)
            user = User.objects.get(pk=pk)
            return (user, None)
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None
