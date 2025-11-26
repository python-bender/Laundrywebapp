from django.urls import path
from . import views, utils  # now utils exists

app_name = 'orders'

urlpatterns = [
    path('', views.new_order, name='new_order'),
    path('order/<int:order_id>/', views.order_detail, name='detail'),
    path('invoice/<int:order_id>/', utils.render_invoice_pdf, name='invoice'),
    path('admin/order/<int:order_id>/', views.admin_order_view, name='admin_detail'),
]