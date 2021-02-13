from django.contrib import admin
from .models import City, Shop, Street


admin.site.register(City)
admin.site.register(Street)
admin.site.register(Shop)

# Register your models here.
