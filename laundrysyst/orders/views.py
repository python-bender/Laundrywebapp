from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import ClothType, Order, OrderItem
from django.urls import reverse
from decimal import Decimal


@login_required
def new_order(request):
    cloths = ClothType.objects.all()
    if request.method == 'POST':
        # build order
        order = Order.objects.create(customer=request.user, total_amount=0)
        total = Decimal('0.00')
        for cloth in cloths:
            q = int(request.POST.get(f'qty_{cloth.id}', 0) or 0)
            if q > 0:
                item = OrderItem.objects.create(
                    order=order,
                    cloth_type=cloth,
                    quantity=q,
                    price=cloth.price
                )
                total += Decimal(q) * cloth.price
        order.total_amount = total
        order.save()
        # redirect to payment init
        return redirect('payments:pay', order_id=order.id)
    return render(request, 'orders/new_order.html', {'cloths': cloths})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/detail.html', {'order': order})




@staff_member_required
def admin_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'receive':
            order.status = 'RECEIVED'
            order.save()
            # generate receipt here or provide download link
            return redirect('admin_orders')
    return render(request, 'orders/admin_detail.html', {'order': order})
