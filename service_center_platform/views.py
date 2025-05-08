from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
    return render(request, 'home.html')

def service_center_list(request):
    return render(request, 'service_centers/list.html')

class ServiceCenterBrandListView(TemplateView):
    template_name = "service_centers/service_center_list.html"