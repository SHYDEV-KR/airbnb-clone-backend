from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Perk
from .serializers import PerkSerializer

class Perks(APIView):
  def get(self, request):
    all_perks = Perk.objects.all()
    serializer = PerkSerializer(
      all_perks, 
      many=True,
    )
    return Response(serializer.data)

  def post(self, request):
    serializer = PerkSerializer(data=request.data)
    if serializer.is_valid():
      return Response(
        PerkSerializer(serializer.save()).data,
      )
    else:
      return Response(serializer.errors)

class PerkDetail(APIView):
  def get_object(self, pk):
    try:
      return Perk.objects.get(pk=pk)
    except Perk.DoesNotExist:
      raise NotFound

  def get(self, request, perk_id):
    serializer = PerkSerializer(self.get_object(perk_id))
    return Response(serializer.data)

  def put(self, request, perk_id):
    serializer = PerkSerializer(
      self.get_object(perk_id),
      data=request.data,
      partial=True,
    )
    if serializer.is_valid():
      return Response(
        PerkSerializer(serializer.save()).data,
      )
    else:
      return Response(serializer.errors)

  def delete(self, request, perk_id):
    self.get_object(perk_id).delete()
    return Response(status=HTTP_204_NO_CONTENT)