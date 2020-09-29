from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count

from taggit.models import Tag

from recipe.forms import ReviewForm
from recipe.models import Recipe, Review


def index(request: HttpRequest):
    return recipes_list(request)


def recipes_list(request: HttpRequest):
    return render(request, 'recipe/recipe_list.html',
                  {'recipes': Recipe.objects.all()})


def recipe(request: HttpRequest, slug):
    return render(request, 'recipe/recipe_detail.html',
                  {'recipe': Recipe.objects.get(slug=slug),
                  'review_form': ReviewForm(),
                  'reviews': Recipe.objects.get(slug=slug).reviews.order_by('-publish_date'),
                  'slug':slug})

def review(request: HttpRequest, slug):
    if request.method == 'GET':
        return HttpResponseNotFound()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review()
            review.user = User.objects.get(username='admin')
            review.comment = form.cleaned_data['comment']
            review.rating = form.cleaned_data['rating']
            review.recipe = Recipe.objects.get(slug=slug)
            review.save()
    return HttpResponseRedirect(review.recipe.get_absolute_url())

def tag_recipe_list(request: HttpRequest, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    return render(request, 'recipe/recipe_list.html', {
        'recipes':  Recipe.objects.filter(tags__in=[tag]),
    })

def search_recipe(request: HttpRequest):
    query = request.GET['query']
    result = Recipe.objects.filter(title__contains=query)
    return render(request, 'recipe/recipe_list.html',
                  {'recipes': result})