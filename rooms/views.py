from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def see_rooms(request):
  return HttpResponse("hello")

def see_room(request, room_id):
  return HttpResponse(f"hello {room_id}")