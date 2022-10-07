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
  owner = MinimalUserSerializer()
  amenities = AmenitySerializer(many=True)
  category = CategorySerializer()

  class Meta:
    model = Room
    fields = "__all__"