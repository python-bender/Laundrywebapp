from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from orders.models import Order
from .models import Payment
from django.conf import settings
from .paystack import initialize_payment
from django.urls import reverse

def pay(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    callback = f"{settings.DOMAIN}{reverse('payments:verify', args=[order.id])}"
    init = initialize_payment(order.customer.email, order.total_amount, callback)
    if init.get('status'):
        auth_url = init['data']['authorization_url']
        reference = init['data']['reference']
        Payment.objects.create(order=order, reference=reference, amount=order.total_amount, status='INITIALIZED')
        return redirect(auth_url)
    else:
        # error
        return render(request, 'payments/error.html', {'message': init.get('message')})

def verify(request, order_id):
    import requests
    from django.conf import settings
    order = get_object_or_404(Order, id=order_id)
    payment = order.payments.last()
    if not payment:
        return render(request, 'payments/error.html', {'message':'No payment found.'})
    url = f"https://api.paystack.co/transaction/verify/{payment.reference}"
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    r = requests.get(url, headers=headers)
    resp = r.json()
    if resp.get('status') and resp['data']['status'] == 'success':
        payment.status = 'SUCCESS'
        from django.utils import timezone
        payment.paid_at = timezone.now()
        payment.save()
        order.status = 'PAID'
        order.save()
        return redirect('orders:detail', order_id=order.id)
    else:
        payment.status = 'FAILED'
        payment.save()
        return render(request, 'payments/error.html', {'message':'Payment verification failed.'})
