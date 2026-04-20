from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/quote/', views.submit_quote, name='submit_quote'),
]