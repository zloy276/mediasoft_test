from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import City, Street, Shop


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'name',
        )


class StreetSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)

    class Meta:
        model = Street
        fields = (
            'name',
            'city',
        )


class ShopSerializer(ModelSerializer):
    # open = serializers.SerializerMethodField()

    street = StreetSerializer(many=False)
    city = CitySerializer(many=False)

    class Meta:
        model = Shop
        fields = (
            'name',
            'street',
            'house',
            'close_time',
            'open_time',
            'city',
            'open'
        )
        read_only_fields = (
            'open',
        )

    # @staticmethod
    # def get_open(self):
    #     if self.open_time < datetime.now().time() < self.close_time:
    #         return 1
    #     return 0
