from django.urls import path
from . import views

urlpatterns = [
    path('service-center/<int:pk>/', views.service_center_detail, name='service_center_detail'),
]
