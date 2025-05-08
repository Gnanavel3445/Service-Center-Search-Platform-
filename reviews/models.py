from django.db import models
from django.contrib.auth.models import User
from django import forms


class ServiceCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    # Other fields...
    reviews = models.ManyToManyField('reviews.Review', related_name='service_centers', blank=True)


class Review(models.Model):
    title = models.CharField(max_length=255)  # Title of the review
    content = models.TextField()  # Content of the review
    rating = models.IntegerField()  # Rating (e.g., 1-5)
    recommend = models.BooleanField(default=False)  # Whether the user recommends the service
    service_date = models.DateField(blank=True, null=True)  # Date of the service
    service_received = models.CharField(max_length=255, blank=True, null=True)  # Type of service received
    comment = models.TextField(blank=True, null=True)  # Optional comment field
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who wrote the review
    service_center = models.CharField(max_length=255)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created

    def __str__(self):
        return f"{self.user} - {self.service_center}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review {self.review.id}"


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} liked review {self.review.id}"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'recommend', 'service_date', 'service_received', 'comment', 'service_center']


class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
