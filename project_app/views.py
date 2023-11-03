from .forms import StoreForm
from .models import Store
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

class StoreListView(generic.ListView):
   model = Store
# class StoreDetailView(generic.DetailView):
#    model = Store
#    def get_context_data(self, **kwargs):
#       context = super(StoreDetailView, self).get_context_data(**kwargs)
#       sheets = Sheets.objects.filter(store_id=self.object)
#       context['sheets'] = sheets
#       return context