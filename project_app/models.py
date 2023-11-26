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

class Sheet(models.Model):
    # Sheet name (required)
    name = models.CharField(max_length=100, blank=False)
    # Sheet author (required)
    author = models.CharField(max_length=50, blank=False)
    # Member to attatch the current date and time when the sheet is created
    pub_date = models.DateTimeField(auto_now_add=True)
    # Additional info (NOT required)
    notes = models.CharField(max_length=100, blank=True)
    # A store can have multiple sheets
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=None)
    # A sheet can have multiple items, items are not unique for a given sheet
    items = models.ManyToManyField('Item', related_name='sheets', blank=True)

    def __str__(self):
        return f'{self.name} - {self.pub_date}'
    
    # Returns the URL to access a particular instance of MyModelName.
    # if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('sheet-detail', args=[self.store.id, self.id])

class Item(models.Model):
    # Sheet name (required)
    name = models.CharField(max_length=100, blank=False)
    # Item barcode image (required)
    barcode = models.ImageField(upload_to='barcode_images/', blank=False)
    # Item code (required)
    code = models.CharField(max_length=100, blank=False)
    # Quantity per bag (NOT required)
    quant_bag = models.CharField(max_length=100, blank=True)
    # Quantity per box (NOT required)
    quant_box = models.CharField(max_length=100, blank=True)
    # Additional info (NOT required)
    about = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])
    