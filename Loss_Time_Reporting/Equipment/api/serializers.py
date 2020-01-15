from rest_framework import serializers
from Equipment.models import Equipment, Locate

class LocateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Locate
        fields = "__all__"

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Equipment
        fields = "__all__"
