from django.db import models
from django.utils import timezone
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

    WEB_Image = 'web_image'
    Local_Image = 'local_image'

    IMAGE_TYPES = (
        (WEB_Image, 'WEB Image'),
        (Local_Image, 'Local or No Image'),
    )

    author = models.ForeignKey('auth.User', default=None, on_delete=models.CASCADE)
    type = models.CharField(max_length=9, choices=ITEM_TYPES, default=UNKNOWN)
    make = models.CharField(max_length=15, default='', blank=False)
    model = models.CharField(max_length=20, default='', blank=False)
    build_year = models.IntegerField(validators=[year_validator])
    description = models.TextField(blank=False)
    image_type = models.CharField(max_length=11, choices=IMAGE_TYPES)
    image_url = models.URLField(blank=True,
                                default='https://s.clipartkey.com/mpngs/s/39-392476_transparent-jeep-clipart-audi-a4-2014-front.png')
    image_file = models.ImageField(blank=True, default='../static/img/car.png', upload_to='images')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


# Additional property db
class Like(models.Model):
    author = models.ForeignKey('auth.User', default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # Helper field to make db visible in admin panel, using "manager class"
    # test = models.CharField(max_length=2)


class Comment(models.Model):
    author = models.ForeignKey('auth.User', default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, max_length=200)
    published = models.DateField()

    def publish(self):
        self.published = timezone.now()
        self.save()
