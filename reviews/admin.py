from django.contrib import admin
from .models import Review

# Register your models here.
class WordFilter(admin.SimpleListFilter):

  title = "positive words!"

  parameter_name = "word"

  def lookups(self, request, model_admin):
    return [
      ("good", "Good"),
      ("great", "Great"),
      ("awesome", "Awesome"),
    ]

  def queryset(self, request, reviews):
    word = self.value()
    if word:
      return reviews.filter(payload__contains=word)
    else:
      reviews

class GoodOrBadReviewFilter(admin.SimpleListFilter):

  title = "good or bad reviews."

  parameter_name = "reviews"

  def lookups(self, request, model_admin):
    return [
      ("good", "Good"),
      ("bad", "Bad"),
    ]

  def queryset(self, request, reviews):
    if self.value() == "good":
      return reviews.filter(rating__gte=3)
    elif self.value() == "bad":
      return reviews.filter(rating__lt=3)
    else:
      reviews

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

  list_display = (
    "__str__",
    "payload",
  )
  list_filter = (
      WordFilter,
      GoodOrBadReviewFilter,
      "rating",
      "user__is_host",
      "room__category",
      "room__pet_friendly",
    )