from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/success/', views.payment_success, name='payment_success'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<str:order_number>/', views.order_detail, name='order_detail'),
]