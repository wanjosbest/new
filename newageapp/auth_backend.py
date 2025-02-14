import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(settings.MONGO_URI)
db = client.get_database("your_database_name")
user_collection = db["users"]  # Adjust collection name

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No authentication, return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user_data = user_collection.find_one({"email": payload["email"]})  # Fetch user from MongoDB

        if not user_data:
            raise AuthenticationFailed("User not found")

        return (MongoUser(user_data), None)  # Return a user-like object

class MongoUser:
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.role = user_data.get("role", "user")  # Default role

    @property
    def is_authenticated(self):
        return True  # Mark user as authenticated
