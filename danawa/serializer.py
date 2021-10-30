from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    co_id = serializers.IntegerField()
    pr_name = serializers.CharField(max_length=30)
    mo_name = serializers.CharField(max_length=30)
    desc = serializers.CharField(max_length=300)
    warranty = serializers.CharField()
    img_path = serializers.CharField(max_length=500)