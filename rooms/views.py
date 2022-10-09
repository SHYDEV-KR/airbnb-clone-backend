from unicodedata import category
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rooms import serializers

# Create your views here.
class Rooms(APIView):
  def get(self, request):
    all_rooms = Room.objects.all()
    serializer = RoomListSerializer(
      all_rooms,
      many=True,
    )
    return Response(serializer.data)

  def post(self, request):
    def get_category_from_request():
        category_pk = request.data.get("category")
        if not category_pk:
          raise ParseError
        try:
          category = Category.objects.get(pk=category_pk)
          if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("The Category kind should be 'rooms'.")
        except Category.DoesNotExist:
          raise ParseError("Category not found.")
        return category

    def add_amenities_to_room_from_request(room):
      amenities = request.data.get("amenities")
      for amenity_pk in amenities:
        amenity = Amenity.objects.get(pk=amenity_pk)
        room.amenities.add(amenity)

    def create_room_with_response(serializer):
        category = get_category_from_request()
        try:
          with transaction.atomic(): ## 오류없이 통과하면 코드 한 번에 실행
            new_room = serializer.save(
              owner=request.user,
              category=category,
            )
            add_amenities_to_room_from_request(new_room)

            return Response(
              RoomDetailSerializer(new_room).data,
            )
        except Exception:
          raise ParseError("Amenity not found.")


    if request.user.is_authenticated:
      serializer = RoomDetailSerializer(data=request.data)
      if serializer.is_valid():
        return create_room_with_response(serializer)
      else:
        return Response(serializer.errors)
    else:
      raise NotAuthenticated


class RoomDetail(APIView):
  def get_object(self, pk):
    try:
      return Room.objects.get(pk=pk)
    except Room.DoesNotExist:
      raise NotFound

  def get(self, request, room_id):
    serializer = RoomDetailSerializer(self.get_object(room_id))
    return Response(serializer.data)

class Amenities(APIView):
  def get(self, request):
    all_amenities = Amenity.objects.all()
    serializer = AmenitySerializer(
      all_amenities,
      many=True,
    )
    return Response(serializer.data)

  def post(self, request):
    serializer = AmenitySerializer(data=request.data)
    if serializer.is_valid():
      new_amenity = serializer.save()
      return Response(
        AmenitySerializer(new_amenity).data,
      )
    else:
      return Response(serializer.errors)

class AmenityDetail(APIView):
  def get_object(self, pk):
    try:
      return Amenity.objects.get(pk=pk)
    except Amenity.DoesNotExist:
      raise NotFound

  def get(self, request, amenity_id):
    serializer = AmenitySerializer(self.get_object(amenity_id))
    return Response(serializer.data)

  def put(self, request, amenity_id):
    serializer = AmenitySerializer(
      self.get_object(amenity_id),
      data = request.data,
      partial=True,
    )
    if serializer.is_valid():
      updated_amenity = serializer.save()
      return Response(
        AmenitySerializer(updated_amenity).data,
      )
    else:
      return Response(serializer.errors)

  def delete(self, request, amenity_id):
    self.get_object(amenity_id).delete()
    return Response(status=HTTP_204_NO_CONTENT)