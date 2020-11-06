from django.urls import path

from .views import *

app_name = 'recipe'

urlpatterns = [
    path('', index, name='recipe_home'),
    path('recipe/user/<username>',
         UserRecipeListView.as_view(), name='user_recipe_list'),
    path('recipe/create', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/search', search_recipe, name='search_recipe'),
    path('recipe/<slug:slug>', recipe, name='recipe'),
    path('recipe/<slug:slug>/review', review, name='review'),
    path('recipe/tag/<slug:tag_slug>', tag_recipe_list, name='tag_recipe_list'),
]
