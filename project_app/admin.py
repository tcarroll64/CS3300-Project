from django.contrib import admin
from .models import Store, Sheet, Item

# # Register your models here so they can be edited in admin panel
admin.site.register(Store)
admin.site.register(Sheet)
admin.site.register(Item)