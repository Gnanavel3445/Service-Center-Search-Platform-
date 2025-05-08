from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from .models import ServiceCenter, Category, ServiceType
from reviews.forms import ReviewForm


class ServiceCenterListView(ListView):
    model = ServiceCenter
    template_name = 'service_centers/service_center_list.html'
    context_object_name = 'service_centers'
    paginate_by = 12

    def get_queryset(self):
        queryset = ServiceCenter.objects.all()

        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filter by service type if provided
        service_type_slug = self.request.GET.get('service_type')
        if service_type_slug:
            queryset = queryset.filter(service_types__slug=service_type_slug)

        # Filter by location if provided
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        state = self.request.GET.get('state')
        if state:
            queryset = queryset.filter(state__icontains=state)

        # Annotate with average rating and review count for sorting
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

        # Sort by different criteria
        sort_by = self.request.GET.get('sort_by', 'featured')
        if sort_by == 'rating':
            queryset = queryset.order_by('-avg_rating', '-review_count', 'name')
        elif sort_by == 'reviews':
            queryset = queryset.order_by('-review_count', '-avg_rating', 'name')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        else:  # Default: featured
            queryset = queryset.order_by('-is_featured', '-avg_rating', 'name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Add current filters to context
        context['current_category'] = self.request.GET.get('category', '')
        context['current_service_type'] = self.request.GET.get('service_type', '')
        context['current_city'] = self.request.GET.get('city', '')
        context['current_state'] = self.request.GET.get('state', '')
        context['current_sort'] = self.request.GET.get('sort_by', 'featured')

        # If category is selected, get related service types
        if context['current_category']:
            category = get_object_or_404(Category, slug=context['current_category'])
            context['service_types'] = category.service_types.all()
            context['current_category_name'] = category.name

        return context


class ServiceCenterDetailView(DetailView):
    model = ServiceCenter
    template_name = 'service_centers/service_center_detail.html'
    context_object_name = 'service_center'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        return context


def category_list(request):
    categories = Category.objects.annotate(service_center_count=Count('service_centers'))
    return render(request, 'service_centers/category_list.html', {'categories': categories})
