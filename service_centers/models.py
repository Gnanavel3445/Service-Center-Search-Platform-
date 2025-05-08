from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fa-car')", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='service_types')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceCenter(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='service_centers')
    service_types = models.ManyToManyField(ServiceType, related_name='service_centers')
    logo = models.ImageField(upload_to='service_center_logos/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='service_center_images/', blank=True, null=True)

    # Contact information
    email = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField()
    website = models.URLField(blank=True, null=True)

    # Address information
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude for map display")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude for map display")

    # Business hours
    monday_hours = models.CharField(max_length=100, blank=True, null=True)
    tuesday_hours = models.CharField(max_length=100, blank=True, null=True)
    wednesday_hours = models.CharField(max_length=100, blank=True, null=True)
    thursday_hours = models.CharField(max_length=100, blank=True, null=True)
    friday_hours = models.CharField(max_length=100, blank=True, null=True)
    saturday_hours = models.CharField(max_length=100, blank=True, null=True)
    sunday_hours = models.CharField(max_length=100, blank=True, null=True)

    # Status and metadata
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_center_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @property
    def review_count(self):
        return self.reviews.count()


class ServiceCenterImage(models.Model):
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_center_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.service_center.name}"