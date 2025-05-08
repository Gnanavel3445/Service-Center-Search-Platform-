from django import forms
from .models import ReviewImage, Review


class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image caption (optional)'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'recommend', 'comment', 'service_date', 'service_received']


def some_view(request):
    from .forms import ReviewForm
    # Use ReviewForm here
