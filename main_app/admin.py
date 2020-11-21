from django.contrib import admin

from main_app.models import Item, Like, Comment

admin.site.register(Item)
admin.site.register(Like)
admin.site.register(Comment)
