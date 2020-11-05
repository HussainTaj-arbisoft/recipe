from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from recipe.models import Recipe, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(),
            'rating': forms.RadioSelect()
        }

class RecipeForm(forms.ModelForm):
    instructions = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Recipe
        fields = '__all__'