from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stock-request/', views.create_stock_request, name='create_stock_request'),
    path('stock-request/<int:request_id>/fulfill/', views.fulfill_stock_request, name='fulfill_stock_request'),
]
