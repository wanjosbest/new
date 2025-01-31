import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return None

        try:
            # Check if the token starts with 'Bearer '
            if token.startswith('Bearer '):
                token = token[7:]

            # Decode the JWT
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # You can get the user information from the decoded token
            user_id = decoded_token.get('user_id')

            # Retrieve the user from the database
            from .models import User  # Import your user model
            user = User.objects.get(id=user_id)

            return (user, None)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

