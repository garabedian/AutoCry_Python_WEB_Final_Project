from django.db import models

from main_app.validators import year_validator


class Item(models.Model):
    SEDAN = 'sedan'
    HATCHBACK = 'hatchback'
    ESTATE = 'ESTATE'
    MPV = 'mpv'
    SUV = 'suv'
    UNKNOWN = 'unknown'

    ITEM_TYPES = (
        (SEDAN, 'SEDAN'),
        (HATCHBACK, 'HATCHBACK'),
        (ESTATE, 'ESTATE'),
        (MPV, 'MPV'),
        (SUV, 'SUV'),
        (UNKNOWN, 'Unknown'),
    )

    type = models.CharField(max_length=9, choices=ITEM_TYPES, default=UNKNOWN)
    make = models.CharField(max_length=15, default='', blank=False)
    model = models.CharField(max_length=20, default='', blank=False)
    build_year = models.IntegerField(validators=[year_validator])
    description = models.TextField(blank=False)
    image_url = models.URLField(blank=False)


# Additional property db
class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # Helper field to make db visible in admin panel, using "manager class"
    # test = models.CharField(max_length=2)


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, max_length=200)
