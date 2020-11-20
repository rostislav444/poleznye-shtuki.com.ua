from django.urls import include, path, re_path
from apps.core import views


app_name = 'core'


pages = [
    path('<slug>/',  views.PageView,  name='page'),
]

urlpatterns = [
    path('page/',  include(pages)),
    path('subscription/', views.subscription, name="subscription")
]
