from django.shortcuts import render
from django.db.models import Q, Avg, Count
from service_centers.models import ServiceCenter, Category
from django.views.generic import ListView


def search_view(request):
    query = request.GET.get('q', '')
    results = ServiceCenter.objects.filter(name__icontains=query) if query else []
    return render(request, 'search/results.html', {'results': results})


class AdvancedSearchView(ListView):
    model = ServiceCenter
    template_name = 'search/advanced_search.html'
    context_object_name = 'service_centers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Add filtering based on GET parameters
        params = self.request.GET

        if 'q' in params and params['q']:
            queryset = queryset.filter(
                Q(name__icontains=params['q']) |
                Q(description__icontains=params['q'])
            )

        if 'category' in params and params['category']:
            queryset = queryset.filter(categories__slug=params['category'])

        if 'service_type' in params and params['service_type']:
            queryset = queryset.filter(service_types__slug=params['service_type'])

        if 'city' in params and params['city']:
            queryset = queryset.filter(city__icontains=params['city'])

        if 'state' in params and params['state']:
            queryset = queryset.filter(state__icontains=params['state'])

        if 'min_rating' in params and params['min_rating']:
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating'))
            queryset = queryset.filter(avg_rating__gte=params['min_rating'])

        # Annotate with rating info for sorting and display
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add all parameters to context for form display
        context.update(self.request.GET.dict())

        # Add categories for filters
        context['categories'] = Category.objects.all()

        # If a category is selected, add related service types
        if 'category' in self.request.GET and self.request.GET['category']:
            category = Category.objects.get(slug=self.request.GET['category'])
            context['service_types'] = category.service_types.all()

        return context
