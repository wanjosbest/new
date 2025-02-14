import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://wanjos:0903620Wanjos@newagedatabase.40ybp.mongodb.net/?retryWrites=true&w=majority&appName=newagedatabase"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['newageadatabase']  # Database name
affiliate_collection = db["affiliate"]
student_collection = db["student"]
tutor_collection = db["tutor"]
admin_collection = db["admin"]

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

        user_data = admin_collection.find_one({"email": payload["email"]}) or affiliate_collection.find_one({"email": payload["email"]}) or student_collection.find_one({"email": payload["email"]}) or tutor_collection.find_one({"email": payload["email"]})

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
