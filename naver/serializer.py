from rest_framework import serializers

class MyProductSerializer(serializers.Serializer):
    mo_name = serializers.CharField(max_length=200)
    purchased_at = serializers.CharField()