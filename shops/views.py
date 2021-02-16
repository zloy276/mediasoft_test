from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.utils.timezone import now
from .serializers import ShopSerializer, CitySerializer, StreetSerializer
from rest_framework import viewsets
from .models import City, Shop, Street
from django.db.models import Q


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

        city = City.objects.filter(name=city_name).first()
        if not city:
            city = City.object.create(name=city_name)

        street = Street.objects.filter(name=street_name, city_=city).first()
        if not street:
            street = Street.object.create(name=street_name, city=city)

        shop = Shop.objects.create(name=name, city=city, street=street, house=house, close_time=close_time,
                                   open_time=open_time)

        return Response({'id': shop.pk})

    def list(self, request):
        city_name = self.request.query_params.get('city', None)
        street_name = self.request.query_params.get('street', None)
        open = int(self.request.query_params.get('open', None))
        if open:
            qs = Shop.objects.filter(city__name=city_name, street__name=street_name, open_time__lt=now(),
                                     close_time__gte=now())
        else:
            qs = Shop.objects.filter(Q(city__name=city_name, street__name=street_name) & (
                        Q(open_time__gt=now()) | Q(close_time__lte=now())))

        serialized = self.get_serializer(qs, many=True)
        return Response(serialized.data)
