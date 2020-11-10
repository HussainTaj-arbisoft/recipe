from rest_framework.serializers import ModelSerializer

from recipe.models import Ingredient, Recipe


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["name", "amount", "unit"]


class RecipeSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ["title", "instructions", "prep_time", "image_url", "ingredients"]
