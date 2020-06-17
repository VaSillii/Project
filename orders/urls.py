from django.urls import path
from .views import SpecialistsListView, order_view, spec_view, my_orders

app_name = "orders"

urlpatterns = [
    path('list-specialists/', SpecialistsListView.as_view(), name='list_specialists'),
    path('order/<int:category_id>/', order_view, name='order_work'),
    path('select-spec/', spec_view, name='select_order'),
    path('my-orders/', my_orders, name='my_order'),
]