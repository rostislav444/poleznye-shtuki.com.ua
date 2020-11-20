from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.order import views


app_name = 'order'


urlpatterns = [
    path('<int:product_id>/<int:variant_id>/',  views.OrderView.as_view(), name='order'),
    path('<int:product_id>/',  views.OrderView.as_view(), name='order'),
    path('',  views.OrderView.as_view(),  name='order'),
    path('success',  TemplateView.as_view(template_name='order/order__success.html'), name='order-success'),
  
]
