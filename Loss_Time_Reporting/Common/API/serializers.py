from rest_framework import serializers
from Common.models import User, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta :
        model = Address
        fields = "__all__"
