import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb+srv://wanjos:0903620Wanjos@newagedatabase.40ybp.mongodb.net/?retryWrites=true&w=majority&appName=newagedatabase"

client = MongoClient(MONGO_URI)
db = client["newagedatabase"]
student_collection = db["student"]
admin_collection = db["admin"]
tutor_collection = db["tutor"]
affiliate_collection = db["affiliate"]

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return None

        try:
            # Check if the token starts with 'Bearer '
            if token.startswith("Bearer "):
                token = token[7:]

            # Decode the JWT
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Get user_id from token
            user_id = decoded_token.get("user_id")

            # Retrieve user from MongoDB
            user = student_collection.find_one({"_id": user_id}) or tutor_collection.find_one({"_id": user_id}) or affiliate_collection.find_one({"_id": user_id}) or admin_collection.find_one({"_id": user_id})
            if not user:
                raise exceptions.AuthenticationFailed("User not found")

            return (user, None)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
