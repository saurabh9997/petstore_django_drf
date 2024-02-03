# pets/urls.py
from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [path('/order', views.StoreListView.as_view(), name='create_order'),
               path('/order/<int:orderId>', views.StoreDetailView.as_view(), name='purchased_order_by_id'),
               path('/inventory', views.StoreInventory.as_view(), name='inventory_by_status')]
