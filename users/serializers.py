from curses.ascii import US
from rest_framework import serializers
from .models import User

class MinimalUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields= (
      "name",
      "avatar",
      "username"
    )