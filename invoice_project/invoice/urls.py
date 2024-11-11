from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),  # Main page for /invoice/
    path('create/', views.create_invoice, name='create_invoice'),  # Reference to create_invoice
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
]
