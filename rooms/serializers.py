from unicodedata import category
from rest_framework import serializers
from .models import Amenity, Room

from users.serializers import MinimalUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Amenity
    fields = (
      "name",
      "description",
    )

class RoomListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields= (
      "pk",
      "name",
      "country",
      "city",
      "price"
    )

class RoomDetailSerializer(serializers.ModelSerializer):
  owner = MinimalUserSerializer(read_only=True)
  amenities = AmenitySerializer(read_only=True, many=True)
  category = CategorySerializer(read_only=True)

  class Meta:
    model = Room
    fields = "__all__"