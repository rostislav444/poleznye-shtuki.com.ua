from django.urls import include, path, re_path
from apps.cart import views


app_name = 'order'


urlpatterns = [
    path('add', views.CartView.as_view({'post' : 'add'}), name="add"),
    path('clear', views.CartView.as_view({'get' : 'clear'}), name="clear"),
    path('update', views.CartView.as_view({'post' : 'update'}), name="update"),
    path('remove/<int:number>', views.CartView.as_view({'get' : 'remove'}), name="remove"),
  
]
