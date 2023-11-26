from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Store, Sheet, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import VALID_PIN

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields =('name', 'store_img', 'about')

class SheetForm(ModelForm):
    class Meta:
        model = Sheet
        fields =('name', 'author', 'notes')

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields =('name', 'barcode', 'code', 'quant_bag', 'quant_box', 'about')

class AddItemsToSheetForm(forms.Form):
    # https://docs.djangoproject.com/en/4.2/ref/forms/fields/#django.forms.ModelMultipleChoiceField
    # The ModelMultipleChoiceField lets you select multiple objects to add to a (many to many) field
    # The CheckboxSelectMultiple adds checkboxes next to each Item object so you can select what to add to the scan sheet
    items = ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

class CreateUserForm(UserCreationForm):
    # Added additional length to the PIN field so if VALID_PIN is of length 4, there is a buffer to make
    # it harder to guess.
    pin = forms.CharField(max_length=(len(VALID_PIN) + 5), required=True, label='PIN' )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'pin']