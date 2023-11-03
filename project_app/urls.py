from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('', views.index, name='index'),

path('stores/', views.StoreListView.as_view(), name= 'stores'),
#path('store/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
]

# Source: https://www.geeksforgeeks.org/python-uploading-images-in-django/
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)