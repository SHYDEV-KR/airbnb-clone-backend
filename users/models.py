from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
  first_name = models.CharField(max_length=150, editable=False)
  last_name = models.CharField(max_length=150, editable=False)
  name = models.CharField(max_length=150, default="")
  is_host = models.BooleanField(default=False)
  date_of_birth = models.DateField(default=datetime.date.today)

