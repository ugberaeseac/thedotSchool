from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='payment-index'),
    path('payment/initiate/<str:name>/<str:email>/', views.initiate, name='payment-initiate'),
    path('payment/verify/', views.verify, name='payment-verify'),
    path('payment/success/<uuid:reference>/', views.success, name='payment-success'),
    path('payment/failed/<uuid:reference>/', views.failed, name='payment-failed')
]
