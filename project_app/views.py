#from .forms import ProjectForm, PortfolioForm
#from .models import Student, Portfolio, Project
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from typing import Any

# Create your views here.
def index(request):
# Render the HTML template index.html with the data in the context variable.
   return HttpResponse('home page')

