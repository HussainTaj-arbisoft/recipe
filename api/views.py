from rest_framework.viewsets import ReadOnlyModelViewSet

from recipe.models import Recipe

from .serializers import RecipeSerializer


class RecipeViewSet(ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
