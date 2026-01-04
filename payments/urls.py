from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='payment-index'),
    path('payment/', views.initiate, name='payment-initiate'),
    path('payment/verify/', views.verify, name='payment-verify')
]
