from .forms import StoreForm, SheetForm, ItemForm , AddItemsToSheetForm, CreateUserForm
from .models import Store, Sheet, Item
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .constants import VALID_PIN
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.
def index(request):
   stores = Store.objects.all()
   #print(stores)
   return render(request, 'project_app/index.html', {'stores':stores})

# View to create new store
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def deleteStore(request, store_id):
    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        store.delete()
        return redirect('index')
    
    context = {'store': store}
    return render(request, 'project_app/store_delete.html', context)

# View to update a sheets detils (name, author, description)
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def updateStore(request, store_id):
  store = get_object_or_404(Store, pk=store_id)
  if request.method == 'POST':
    form = StoreForm(request.POST, instance = store)
    if form.is_valid():
      form.save()
      return redirect('store-detail', pk=store_id)
  else:
    form = StoreForm(instance=store)
    context={'form': form, 'store': store}
  return render(request, 'project_app/store_update.html', context)

# View to create a new sheet
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def deleteSheet(request, store_id, sheet_id):
    sheet = get_object_or_404(Sheet, pk=sheet_id)
    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        sheet.delete()
        return redirect('store-detail', pk=sheet.store.id)
    
    context = {'sheet': sheet, 'store':store}
    return render(request, 'project_app/sheet_delete.html', context)

# View to add an item to a sheet from sheet detail page
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def addItemsToSheet(request, sheet_id, store_id):
   sheet = get_object_or_404(Sheet, pk=sheet_id)
   store = get_object_or_404(Store, pk=store_id)
   items = Item.objects.all()

   if request.method == 'POST':
      form = AddItemsToSheetForm(request.POST, initial={'items': sheet.items.all()})
      if form.is_valid():
         selected_items = form.cleaned_data['items']
         sheet.items.set(selected_items)
         #form.save()
         return redirect('sheet-detail', store_id, sheet_id)
   else:
      form = AddItemsToSheetForm(initial={'items': sheet.items.all()})
   context={'form': form, 'sheet': sheet, 'store':store, 'items':items}
   return render(request, 'project_app/add_items_to_sheet.html', context)

# Had to create a custom detial view because the generic view was not working
def sheet_detail(request, store_id, sheet_id):
    # Retrieve the sheet object using get_object_or_404 to handle 404 errors
    sheet = get_object_or_404(Sheet, pk=sheet_id)
    store = get_object_or_404(Store, pk=store_id)
    items = sheet.items.all()
    context = {'sheet': sheet, 'store': store, 'items': items}
    
    return render(request, 'project_app/sheet_detail.html', context)

# View to create a new item
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
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

def registerPage(request):
   form = CreateUserForm()

   if request.method == 'POST':
      form = CreateUserForm(request.POST)
      pin = request.POST.get('pin', '') # Get the pin entered in on the form

      if pin == VALID_PIN and form.is_valid():
         user = form.save()
         username = form.cleaned_data.get('username')
         group = Group.objects.get(name='supervisor')
         user.groups.add(group)
         login(request, user)
         messages.success(request, 'Account was created for ' + username)
         return redirect('index')
      else:
         form.add_error('pin', 'Invalid supervisor PIN. Please enter a valid PIN.')
   context = {'form':form}
   return render(request, 'registration/register.html', context)

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

# This view converts the template specified as 'template_path' and renders it as PDF.
# Since the request is a get, no need to verify, no need to use it. Although view must accept the request since its a view.
def generatePDF(request, sheet_id):
   template_path = 'project_app/item_table.html'
   sheet = get_object_or_404(Sheet, pk=sheet_id)
   items = sheet.items.all()

   context = {'items':items, 'sheet': sheet}

   # Loading the template and rendering it
   template = get_template(template_path)
   html = template.render(context)

   # Specifying to use the applications (browser) built-in PDF viewer
   response = HttpResponse(content_type='application/pdf')

   # Naming the PDF file
   response['Content-Disposition'] = f'filename="items_in_sheet_{sheet_id}.pdf"'

   # Using pisa to create a pdf based on the rendered template, destination of the pdf is the HTTP response (the browsers PDF viewer)
   pisa_status = pisa.CreatePDF(html, dest=response)

   # If the PDF couldnt be created give an error, else display the PDF in the browser
   if pisa_status.err:
      return HttpResponse('Errors in html <pre>' + html + ' </pre>')
   else:
      return response