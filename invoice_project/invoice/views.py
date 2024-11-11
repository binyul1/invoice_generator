from django.shortcuts import render, redirect
from .models import Customer, Invoice, Item
from .forms import CustomerForm, ItemFormSet
from django.utils import timezone


from datetime import timedelta


def create_invoice(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        item_formset = ItemFormSet(request.POST)

        if customer_form.is_valid() and item_formset.is_valid():
            # Save customer object
            customer = customer_form.save()

            # Set due_date, either from the form or a default value
            due_date = request.POST.get('due_date') or (timezone.now().date() + timedelta(days=30))

            # Calculate the total_amount from the formset items
            items = item_formset.save(commit=False)
            total_amount = 0

            # Create the invoice first, to ensure each item can be associated with it
            invoice = Invoice.objects.create(
                customer=customer,
                due_date=due_date,
                total_amount=total_amount  # Initialize with 0, we'll update this later
            )

            # Now associate the items with the invoice
            for item in items:
                item.invoice = invoice  # Set the foreign key to the created invoice
                total_amount += item.total_price()  # Add the total price of this item to the invoice total
                item.save()  # Save the item with the associated invoice
                #print("Item saved with description:", item.description)  # Debugging

            # Now update the invoice with the correct total_amount
            invoice.total_amount = total_amount
            invoice.save()

            return redirect('invoice_detail', pk=invoice.pk)

    else:
        customer_form = CustomerForm()
        item_formset = ItemFormSet()

    return render(request, 'invoice/create_invoice.html', {
        'customer_form': customer_form,
        'item_formset': item_formset,
    })


def invoice_list(request):
    invoices = Invoice.objects.all()  # Retrieve all invoices
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})

def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    items = Item.objects.filter(invoice=invoice)  # Retrieve items associated with the invoice
    print("Items for invoice:", items)  # Debugging
    return render(request, 'invoice/invoice_detail.html', {'invoice': invoice, 'items': items})
