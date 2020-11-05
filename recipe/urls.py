from django.urls import path

from .views import *

app_name = 'recipe'

urlpatterns = [
    path('', index, name='home'),
    path('recipe/search', search_recipe, name='search_recipe'),
    path('recipe/<slug:slug>', recipe, name='recipe'),
    path('recipe/<slug:slug>/review', review, name='review'),
    path('recipe/tag/<slug:tag_slug>', tag_recipe_list, name='tag_recipe_list'),
]
