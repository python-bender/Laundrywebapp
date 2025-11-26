from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from .models import Order

def render_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html_string = render_to_string('orders/invoice.html', {'order': order})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    result = html.write_pdf()
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.id}.pdf'
    return response
