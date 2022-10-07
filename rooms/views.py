from django.http import request
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Amenity, Room
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