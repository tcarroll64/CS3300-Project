from .forms import StoreForm, SheetForm, ItemForm ,AddItemsToSheetForm
from .models import Store, Sheet, Item
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from typing import Any

# Create your views here.
def index(request):
   stores = Store.objects.all()
   print(stores)
   return render(request, 'project_app/index.html', {'stores':stores})

# View to create new store
def createStore(request):
   if request.method == 'POST':
      form = StoreForm(request.POST, request.FILES) # request.FILES to handle file upload
      if form.is_valid():
         store = form.save()
         # Redirect back to the landing page (index)
         return redirect('index')
   else:
      form = StoreForm()
   context = {'form': form}
   return render(request, 'project_app/store_form.html', context)

# View to delete a store from the landing page (index)
def deleteStore(request, store_id):
    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        store.delete()
        return redirect('index')
    
    context = {'store': store}
    return render(request, 'project_app/store_delete.html', context)

# View to create a new sheet
def createSheet(request, store_id):
    form = SheetForm()
    store = Store.objects.get(pk=store_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        sheet_data = request.POST.copy()
        sheet_data['store_id'] = store_id
        
        form = SheetForm(sheet_data)
        if form.is_valid():
            # Save the form without committing to the database
            sheet = form.save(commit=False)
            # Set the sheet relationship
            sheet.store = store
            sheet.save()

            # Redirect back to the portfolio detail page
            return redirect('store-detail', store_id)

    context = {'form': form, 'store':store}
    return render(request, 'project_app/sheet_form.html', context)

# View to update a sheets detils (name, author, description)
def updateSheet(request, sheet_id, store_id):
  sheet = get_object_or_404(Sheet, pk=sheet_id)
  store = get_object_or_404(Store, pk=store_id)
  if request.method == 'POST':
    form = SheetForm(request.POST, instance = sheet)
    if form.is_valid():
      form.save()
      return redirect('store-detail', pk=store_id)
  else:
    form = SheetForm(instance=sheet)
    context={'form': form, 'store': store, 'sheet': sheet}
  return render(request, 'project_app/sheet_update.html', context)

# View to delete a sheet from store detail page
def deleteSheet(request, store_id, sheet_id):
    sheet = get_object_or_404(Sheet, pk=sheet_id)
    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        sheet.delete()
        return redirect('store-detail', pk=sheet.store.id)
    
    context = {'sheet': sheet, 'store':store}
    return render(request, 'project_app/sheet_delete.html', context)

# View to add an item to a sheet from sheet detail page
def addItemsToSheet(request, sheet_id, store_id):
   sheet = get_object_or_404(Sheet, pk=sheet_id)
   store = get_object_or_404(Store, pk=store_id)

   if request.method == 'POST':
      form = AddItemsToSheetForm(request.POST, instance=sheet)
      if form.is_valid():
         form.save()
         return redirect('sheet-detail', store_id, sheet_id)
   else:
      form = AddItemsToSheetForm(instance=sheet)
   context={'form': form, 'sheet': sheet, 'store':store}
   return render(request, 'project_app/add_items_to_sheet.html', context)

# Had to create a custom detial view because the generic view was not working
def sheet_detail(request, sheet_id, store_id):
    # Retrieve the sheet object using get_object_or_404 to handle 404 errors
    sheet = get_object_or_404(Sheet, pk=sheet_id)
    store = get_object_or_404(Store, pk=store_id)
    items = sheet.items.all()
    context = {'sheet': sheet, 'store': store, 'items': items}
    
    return render(request, 'project_app/sheet_detail.html', context)

# View to create a new item
def createItem(request):
   if request.method == 'POST':
      form = ItemForm(request.POST, request.FILES)
      if form.is_valid():
         item = form.save()
         return redirect('item-list') # What is the redirect here (cardview of all items)
   else:
      form = ItemForm()
   context = {'form': form}
   return render(request, 'project_app/item_form.html', context)

# View to update an item
def updateItem(request, item_id):
   item = get_object_or_404(Item, pk=item_id)
   if request.method == 'POST':
      form = ItemForm(request.POST, instance = item)
      if form.is_valid():
         form.save()
         return redirect('item-list')
   else:
      form = ItemForm(instance=item)
      context={'form': form, 'item': item}
   return render(request, 'project_app/item_update.html', context)

# Had to create a custom item list view because the generic wasnt working
def item_list(request):
   items = Item.objects.all()
   context = {'items': items}
   return render(request, 'project_app/item_list.html', context)

class StoreListView(generic.ListView):
   model = Store
class StoreDetailView(generic.DetailView):
   model = Store
   def get_context_data(self, **kwargs):
      context = super(StoreDetailView, self).get_context_data(**kwargs)
      sheets = Sheet.objects.filter(store_id=self.object)
      context['sheets'] = sheets
      return context
class SheetListView(generic.ListView):
   model = Sheet
# class ItemListView(generic.ListView):
#    model = Item
class ItemDetailView(generic.DetailView):
   model = Item