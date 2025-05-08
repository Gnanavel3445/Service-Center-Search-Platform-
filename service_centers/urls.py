from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServiceCenterListView.as_view(), name='service_center_list'),
    path('categories/', views.category_list, name='category_list'),
    path('<slug:slug>/', views.ServiceCenterDetailView.as_view(), name='service_center_detail'),
]
