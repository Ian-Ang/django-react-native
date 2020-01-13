from rest_framework import serializers
from Activity.models import Status, Activity

class StatusSerializer(serializers.ModelSerializer):
    class Meta :
        model = Status
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    class Meta :
        model = Activity
        fields = "__all__"
