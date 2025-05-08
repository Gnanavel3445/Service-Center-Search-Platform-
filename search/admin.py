from django.contrib import admin
from .models import SearchQuery


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
