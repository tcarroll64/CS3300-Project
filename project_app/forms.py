from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Store, Sheet, Item

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

class AddItemsToSheetForm(ModelForm):
    class Meta:
        model = Sheet
        fields = ['items']

    # https://docs.djangoproject.com/en/4.2/ref/forms/fields/#django.forms.ModelMultipleChoiceField
    # The ModelMultipleChoiceField adds checkboxes next to each Item object so you can select what to add to the scan sheet
    items = ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )