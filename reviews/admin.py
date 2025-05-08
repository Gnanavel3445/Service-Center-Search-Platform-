from django.contrib import admin
from .models import Review, ReviewImage, ReviewLike


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']  # Ensure 'created_at' exists in the model
    list_display = ['service_center', 'user', 'rating', 'created_at']  # Ensure all fields exist


admin.site.register(Review, ReviewAdmin)


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'caption', 'created_at')
    search_fields = ('review__title', 'caption')


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'review__title')
