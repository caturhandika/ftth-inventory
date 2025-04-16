from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Warehouse, Product, Stock, StockRequest, StockRequestItem, FulfilledItemSerial
from .forms import StockRequestForm, StockRequestItemForm, FulfilledItemSerialForm

def dashboard(request):
    stock_summary = Stock.objects.select_related('product', 'warehouse')
    return render(request, 'inventory/dashboard.html', {
        'stock_summary': stock_summary,
    })

def create_stock_request(request):
    StockRequestItemFormSet = modelformset_factory(
        StockRequestItem, form=StockRequestItemForm, extra=1
    )

    if request.method == 'POST':
        form = StockRequestForm(request.POST)
        formset = StockRequestItemFormSet(request.POST, queryset=StockRequestItem.objects.none())

        if form.is_valid() and formset.is_valid():
            stock_request = form.save(commit=False)
            stock_request.requested_by = request.user
            stock_request.save()

            for item_form in formset:
                item = item_form.save(commit=False)
                item.request = stock_request
                item.save()

            return redirect('dashboard')
    else:
        form = StockRequestForm()
        formset = StockRequestItemFormSet(queryset=StockRequestItem.objects.none())

    return render(request, 'inventory/stock_request_form.html', {
        'form': form,
        'formset': formset,
    })

def fulfill_stock_request(request, request_id):
    stock_request = get_object_or_404(StockRequest, id=request_id)
    StockRequestItemFormSet = modelformset_factory(
        StockRequestItem, form=FulfilledItemSerialForm, extra=0
    )
    queryset = StockRequestItem.objects.filter(request=stock_request)

    if request.method == 'POST':
        formset = StockRequestItemFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            for form in formset:
                item = form.save(commit=False)
                item.save()

                # Add serial numbers if applicable
                for serial_form in form.cleaned_data.get('serial_number', []):
                    FulfilledItemSerial.objects.create(
                        stock_request_item=item,
                        serial_number=serial_form
                    )

                # Deduct quantity from stock based on fulfillment
                stock = Stock.objects.filter(product=item.product).first()
                if stock:
                    stock.quantity -= item.fulfilled_quantity or 0
                    stock.save()

            stock_request.status = 'fulfilled'
            stock_request.save()
            messages.success(request, "Stock request fulfilled successfully.")
            return redirect('dashboard')
    else:
        formset = StockRequestItemFormSet(queryset=queryset)

    return render(request, 'inventory/fulfill_stock_request.html', {
        'stock_request': stock_request,
        'formset': formset,
    })
