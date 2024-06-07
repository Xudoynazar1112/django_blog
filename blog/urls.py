from django.urls import path
from .views import home, post_detail, post_create, register

app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('register/', register, name='register'),
]