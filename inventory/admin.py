from django.contrib import admin
from .models import Warehouse, Product, Stock, StockRequest, StockRequestItem

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockRequest)
admin.site.register(StockRequestItem)