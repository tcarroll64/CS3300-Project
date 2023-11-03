from django.db import models
from django.urls import reverse

# Create your models here.
class Store(models.Model):
    # Store name (required field)
    name = models.CharField(max_length=100, blank=False)
    # Store logo (required field)
    store_img = models.ImageField(upload_to='store_images/', blank=False)
    # Store description (NOT required)
    about = models.CharField(max_length=200, blank=True)

    # Default string to return the name of the store to represent the model object
    def __str__(self):
        return self.name
    
    # Returns the URL to access a particular instance of MyModelName.
    # if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('store-detail', args=[str(self.id)])

