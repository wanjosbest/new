from rest_framework import serializers
from .models import AffiliateWallet


class Studentregister(serializers.Serializer):
    
    firstname =serializers.CharField(max_length=50,)
    lastname =serializers.CharField(max_length=50,)
    username =serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)
    address=serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    course = serializers.CharField(max_length=50, required = True)
    password_confirm = serializers.CharField(max_length=255) 
    dob = serializers.CharField(max_length=50, required = True)
    phonenumber = serializers.CharField(max_length=50, required = True)
    gender = serializers.CharField(max_length=50, required = True)
   
    
    def create(self, validated_data):
        user = super(Studentregister, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    def validate(self, data):
        # Check if the passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        return data

# tutor serializer
class Tutorregister(serializers.Serializer):
    firstname =serializers.CharField(max_length=50,)
    lastname =serializers.CharField(max_length=50,)
    username =serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)
    address=serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    course = serializers.CharField(max_length=50, required = True)
    password_confirm = serializers.CharField(max_length=255) 
    dob = serializers.CharField(max_length=50, required = True)
    phonenumber = serializers.CharField(max_length=50, required = True)
    gender = serializers.CharField(max_length=50, required = True)

    def create(self, validated_data):
        user = super(Studentregister, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    def validate(self, data):
        # Check if the passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        return data


# tutor serializer
class Adminregister(serializers.Serializer):
    firstname =serializers.CharField(max_length=50,)
    lastname =serializers.CharField(max_length=50,)
    username =serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)
    address=serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    course = serializers.CharField(max_length=50, required = True)
    password_confirm = serializers.CharField(max_length=255) 
    dob = serializers.CharField(max_length=50, required = True)
    phonenumber = serializers.CharField(max_length=50, required = True)
    gender = serializers.CharField(max_length=50, required = True)

    def create(self, validated_data):
        user = super(Studentregister, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    def validate(self, data):
        # Check if the passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        return data


# tutor serializer
class Affiliateregister(serializers.Serializer):
    firstname =serializers.CharField(max_length=50,)
    lastname =serializers.CharField(max_length=50,)
    username =serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)
    address=serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    course = serializers.CharField(max_length=50, required = True)
    password_confirm = serializers.CharField(max_length=255) 
    dob = serializers.CharField(max_length=50, required = True)
    phonenumber = serializers.CharField(max_length=50, required = True)
    gender = serializers.CharField(max_length=50, required = True)

    def create(self, validated_data):
        user = super(Studentregister, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    def validate(self, data):
        # Check if the passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        return data
class AffiliateWalletSerializer(serializers.Serializer):
      affiliate_id = serializers.CharField(max_length=255,)
      balance = serializers.DecimalField(max_digits=10, decimal_places = 2)

      def create (self, validated_data):
          affiliate_wallet = AffiliateWallet(validated_data["affiliate_id"], validated_data["balance"])
          affiliate_wallet.save()
          return affiliate_wallet()


      def update(self, instance, validated_data):
          instance.affiliate_id = validated_data.get("affiliate_id",instance.affiliate_id)
          instance.balance = validated_data.get("balance", instance.balance)
          instance.save()
          return instance

          
