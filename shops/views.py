from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .serializers import ShopSerializer, CitySerializer, StreetSerializer
from rest_framework import viewsets
from .models import City, Shop, Street


class CitySet(ListAPIView):
    queryset = City.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    def get_queryset(self):
        qs = City.objects.all()
        return qs


class StreetSet(GenericViewSet):
    queryset = Street.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StreetSerializer

    def list(self, request, *args, **kwargs):
        id = self.request.query_params.get('city_id', None)
        qs = Street.objects.filter(city_id=id).all()
        serialized = self.get_serializer(qs, many=True)
        return Response(serialized.data)


class ShopSet(GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city_name = serializer.validated_data['city']
        street_name = serializer.validated_data['street']
        name = serializer.validated_data['name']
        house = serializer.validated_data['house']
        close_time = serializer.validated_data['close_time']
        open_time = serializer.validated_data['open_time']

        if City.objects.filter(name=serializer.validated_data['city']).exists:
            city = City.objects.filter(name=city_name).first()

            if Street.objects.filter(name=street_name, city=city).exists():
                street = Street.objects.filter(name=street_name, city=city).first()
            else:
                street = Street.objects.create(name=street_name, city=city)

        else:
            city = City.object.create(name=city_name)
            street = Street.objects.create(name=street_name, city=city)

        if not (Shop.objects.filter(name=name, city=city, street=street, house=house).exists()):
            shop = Shop.objects.create(name=name, city=city, street=street, house=house, close_time=close_time,
                                       open_time=open_time)
        else:
            shop = Shop.objects.filter(name=name, city=city, street=street, house=house).first()

        return Response({'id': shop.pk})

    def list(self, request):
        city_name = self.request.query_params.get('city', None)
        street_name = self.request.query_params.get('street', None)
        open = self.request.query_params.get('open', None)

        city = City.objects.filter(name=city_name).first()

        street = Street.objects.filter(name=street_name).first()

        # qs = Shop.objects.filter(city=city, street=street).all()
        qs = []
        for obj in Shop.objects.all():
            if obj.open() == int(open):
                qs.append({
                    'name': obj.name,
                    'city': obj.city.name,
                    'street': obj.street.name,
                    'house': obj.house,
                    'open_time': obj.open_time,
                    'close_time': obj.close_time,
                    'open': open,
                })
        print(qs)
        # serialized = self.get_serializer(qs, many=True)
        return Response(qs)
