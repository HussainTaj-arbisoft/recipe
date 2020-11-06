from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from recipe.models import Recipe, Review, Ingredient


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
        exclude = ['author']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'amount', 'unit']


RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient, IngredientForm)
