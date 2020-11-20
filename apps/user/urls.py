from django.urls import path, re_path 
from apps.user import views

app_name = "user"

urlpatterns = [
    path('login',  views.UserViewset.as_view({'get':'login', 'post':'login'}), name="login"),
    path('profile', views.UserViewset.as_view({'get':'profile', 'post':'profile'}), name="profile"),
    path('register', views.UserViewset.as_view({'get':'register', 'post':'register'}), name="register"),
]