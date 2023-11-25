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
path('store/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
path('sheets/', views.SheetListView.as_view(), name='sheets'),
path('store/<int:store_id>/sheet/<int:sheet_id>', views.sheet_detail, name='sheet-detail'),
path('items/', views.item_list, name='item-list'),
path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
path('store/<int:store_id>/create_sheet', views.createSheet, name='create_sheet'),
path('store/<int:store_id>/update_sheet/<int:sheet_id>', views.updateSheet, name='update-sheet'),
path('store/<int:store_id>/delete_sheet/<int:sheet_id>', views.deleteSheet, name='delete-sheet'),
path('store/<int:store_id>/add_items_to_sheet/<int:sheet_id>', views.addItemsToSheet, name='add_items_to_sheet'),
path('create_store/', views.createStore, name='create_store'),
path('delete_store/<int:store_id>', views.deleteStore, name='delete_store'),
path('update_store/<int:store_id>', views.updateStore, name='update_store'),
path('items/create_item/', views.createItem, name='create_item'),
path('items/update_item/<int:item_id>', views.updateItem, name='update_item'),
path('accounts/register/', views.registerPage, name='register_page'),
]

# Source: https://www.geeksforgeeks.org/python-uploading-images-in-django/
# This looks for images in the MEDIA_ROOT (config in settings) folder whenever <image_path>.url is referenced
# Images are stored on local machine, this is something that should be reconsidered for sprint02
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)