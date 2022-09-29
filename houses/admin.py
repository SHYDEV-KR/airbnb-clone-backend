from django.contrib import admin
from .models import House

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
  list_display = ("name", "price_per_night")
  list_filter = ("price_per_night", )
  search_fields = ("address",)