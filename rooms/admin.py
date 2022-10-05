from django.contrib import admin
from .models import Room, Amenity

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  list_display = (
    "name",
    "price",
    "kind",
    "total_amenities",
    "rating",
    "owner",
    "created_at",
  )

  list_filter = (
    "country",
    "city",
    "pet_friendly",
    "kind",
    "amenities",
    "created_at",
    "updated_at",
  )
  search_fields = (
    "name",
    "^price",
    "=owner__username",
  )

  def total_amenities(self, room):
    return room.amenities.count()

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
  pass