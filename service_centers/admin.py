from django.contrib import admin
from .models import Category, ServiceType, ServiceCenter, ServiceCenterImage


class ServiceCenterImageInline(admin.TabularInline):
    model = ServiceCenterImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'phone_number', 'is_verified', 'is_featured')
    list_filter = ('is_verified', 'is_featured', 'state', 'city', 'categories')
    search_fields = ('name', 'description', 'address', 'city', 'state', 'email')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories', 'service_types')
    inlines = [ServiceCenterImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'categories', 'service_types', 'logo', 'featured_image'),
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number', 'website'),
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country', 'latitude', 'longitude'),
        }),
        ('Business Hours', {
            'fields': ('monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours',
                      'friday_hours', 'saturday_hours', 'sunday_hours'),
        }),
        ('Status', {
            'fields': ('is_verified', 'is_featured'),
        }),
    )


@admin.register(ServiceCenterImage)
class ServiceCenterImageAdmin(admin.ModelAdmin):
    list_display = ('service_center', 'alt_text', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('service_center__name', 'alt_text')
