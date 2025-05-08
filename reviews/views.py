import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_POST
from service_centers.models import ServiceCenter
from .models import Review, ReviewImage, ReviewLike, EmailOTP
from .forms import ReviewForm, ReviewImageForm


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user):
    otp = generate_otp()
    EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp, 'is_verified': False})
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'noreply@example.com',
        [user.email],
    )


@login_required
def add_review(request, service_center_slug):
    service_center = get_object_or_404(ServiceCenter, slug=service_center_slug)

    # Check if user already reviewed this service center
    existing_review = Review.objects.filter(service_center=service_center, user=request.user).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this service center. You can edit your existing review.")
        return redirect('edit_review', review_id=existing_review.id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        image_form = ReviewImageForm(request.POST, request.FILES)

        if review_form.is_valid():
            with transaction.atomic():
                # Save the review
                review = review_form.save(commit=False)
                review.service_center = service_center
                review.user = request.user
                review.save()

                # Handle uploaded images
                if 'image' in request.FILES:
                    for image in request.FILES.getlist('image'):
                        ReviewImage.objects.create(review=review, image=image)

            messages.success(request, "Your review has been submitted successfully!")
            return redirect('service_center_detail', slug=service_center_slug)
    else:
        review_form = ReviewForm()
        image_form = ReviewImageForm()

    return render(request, 'reviews/add_review.html', {
        'review_form': review_form,
        'image_form': image_form,
        'service_center': service_center
    })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()

            # Handle uploaded images
            if 'image' in request.FILES:
                for image in request.FILES.getlist('image'):
                    ReviewImage.objects.create(review=review, image=image)

            messages.success(request, "Your review has been updated successfully!")
            return redirect('service_center_detail', slug=review.service_center.slug)
    else:
        review_form = ReviewForm(instance=review)

    review_images = review.images.all()

    return render(request, 'reviews/edit_review.html', {
        'review_form': review_form,
        'review': review,
        'review_images': review_images,
        'service_center': review.service_center
    })


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    service_center_slug = review.service_center.slug
    review.delete()
    messages.success(request, "Your review has been deleted successfully!")
    return redirect('service_center_detail', slug=service_center_slug)


@login_required
@require_POST
def delete_review_image(request, image_id):
    image = get_object_or_404(ReviewImage, id=image_id, review__user=request.user)
    image.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(review=review, user=request.user)

    if not created:
        # User already liked the review, so unlike it
        like.delete()
        liked = False
    else:
        liked = True

    like_count = review.likes.count()

    return JsonResponse({
        'liked': liked,
        'likeCount': like_count
    })


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:list')  # Replace with your desired redirect URL
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form})


def service_center_detail(request, pk):
    service_center = get_object_or_404(ServiceCenter, pk=pk)
    return render(request, 'service_centers/service_center_detail.html', {'service_center': service_center})
