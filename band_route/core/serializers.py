from rest_framework import serializers


class CityListSerializer(serializers.Serializer):
    """Serialize city objects"""

    x = serializers.IntegerField()
    y = serializers.IntegerField()
