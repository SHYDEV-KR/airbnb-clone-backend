from unicodedata import category
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer

from rooms import serializers

# Create your views here.
def get_validated_category(category_pk):
    try:
      category = Category.objects.get(pk=category_pk)
      if category.kind == Category.CategoryKindChoices.EXPERIENCES:
        raise ParseError("The Category kind should be 'rooms'.")
    except Category.DoesNotExist:
      raise ParseError("Category not found.")
    return category

class Rooms(APIView):
  def get(self, request):
    all_rooms = Room.objects.all()
    serializer = RoomListSerializer(
      all_rooms,
      many=True,
      context={"request": request},
    )
    return Response(serializer.data)

  def post(self, request):
    def get_category_from_request(request):
      category_pk = request.data.get("category")
      if not category_pk:
        raise ParseError
      category = get_validated_category(category_pk)
      return category

    def add_amenities_to_room_from_request(request, room):
      amenities = request.data.get("amenities")
      for amenity_pk in amenities:
        amenity = Amenity.objects.get(pk=amenity_pk)
        room.amenities.add(amenity)

    def create_room_with_response(serializer):
        category = get_category_from_request(request)
        try:
          with transaction.atomic(): ## 오류없이 통과하면 코드 한 번에 실행
            new_room = serializer.save(
              owner=request.user,
              category=category,
            )
            add_amenities_to_room_from_request(request, new_room)

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
    serializer = RoomDetailSerializer(
      self.get_object(room_id),
      context={"request": request},
    )
    return Response(serializer.data)

  def put(self, request, room_id):
    def update_room_with_response(serializer):
      category_pk = request.data.get("category")
      if category_pk:
        category = get_validated_category(category_pk)

      try:
        with transaction.atomic(): ## 오류없이 통과하면 코드 한 번에 실행  
          if category_pk:
            room = serializer.save(
              category=category,
            )
          else:
            room = serializer.save()
            
          amenities = request.data.get("amenities")
          if amenities:
            room.amenities.clear()
            for amenity_pk in amenities:
              amenity = Amenity.objects.get(pk=amenity_pk)
              room.amenities.add(amenity)
          elif amenities is not None:
            room.amenities.clear()

          return Response(
            RoomDetailSerializer(room).data,
          )
      except Exception:
        raise ParseError("Amenity not found.")

    room = self.get_object(room_id)
    if not request.user.is_authenticated:
      raise NotAuthenticated
    if room.owner != request.user:
      raise PermissionDenied

    serializer = RoomDetailSerializer(
      self.get_object(room_id),
      data = request.data,
      partial=True,
    )
    if serializer.is_valid():
      return update_room_with_response(serializer)
    else:
      return Response(serializer.errors)

  def delete(self, request, room_id):
    room = self.get_object(room_id)
    if not request.user.is_authenticated:
      raise NotAuthenticated
    if room.owner != request.user:
      raise PermissionDenied
    
    room.delete()
    return Response(status=HTTP_204_NO_CONTENT)


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


class RoomReviews(APIView):
  def get_object(self, pk):
    try:
      return Room.objects.get(pk=pk)
    except Room.DoesNotExist:
      raise NotFound

  def get(self, request, room_id):
    try:
      page = int(request.query_params.get("page", 1))
    except ValueError:
      page = 1
    page_size = 5
    start = (page - 1) * page_size
    end = start + page_size
    room = self.get_object(room_id)
    serializer = ReviewSerializer(
      room.reviews.all()[start:end],
      many=True,
    )
    return Response(serializer.data)

class RoomAmenities(APIView):
  def get_object(self, pk):
    try:
      return Room.objects.get(pk=pk)
    except Room.DoesNotExist:
      raise NotFound

  def get(self, request, room_id):
    try:
      page = int(request.query_params.get("page", 1))
    except ValueError:
      page = 1
    page_size = 5
    start = (page - 1) * page_size
    end = start + page_size
    room = self.get_object(room_id)
    serializer = AmenitySerializer(
      room.amenities.all()[start:end],
      many=True,
    )
    return Response(serializer.data)