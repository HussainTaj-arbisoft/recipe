from django.urls import path

from .views import *

app_name = 'recipe'

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_home'),
    path('recipe/user/<username>',
         UserRecipeListView.as_view(), name='user_recipe_list'),
    path('recipe/create', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/search', SearchRecipeListView.as_view(), name='search_recipe'),
    path('recipe/<slug:slug>', recipe, name='recipe'),
    path('recipe/<slug:slug>/review', review, name='review'),
    path('recipe/tag/<slug:tag_slug>',
         TagRecipeListView.as_view(), name='tag_recipe_list'),
]
