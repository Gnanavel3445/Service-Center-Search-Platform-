from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('advanced/', views.AdvancedSearchView.as_view(), name='advanced_search'),
]
