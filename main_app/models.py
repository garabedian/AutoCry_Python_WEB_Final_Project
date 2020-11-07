from django.db import models


# Create your models here.
# Info db
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
    name = models.CharField(max_length=10, blank=False)
    age = models.PositiveIntegerField(blank=False)
    description = models.TextField(blank=False)
    image_url = models.URLField(blank=False)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.age}'


# Additional property db
class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # Helper field to make db visible in admin panel, using "manager class"
    test = models.CharField(max_length=2)


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, max_length=200)
