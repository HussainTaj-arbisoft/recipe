from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from recipe.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(),
            'rating': forms.RadioSelect()
        }