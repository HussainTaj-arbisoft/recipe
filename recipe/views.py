from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from taggit.models import Tag

from recipe.forms import ReviewForm
from recipe.models import Recipe, Review


def index(request: HttpRequest):
    return recipes_list(request)


def recipes_list(request: HttpRequest):
    return render(request, 'recipe/recipe_list.html',
                  {'recipes': Recipe.objects.all()})


def recipe(request: HttpRequest, slug):
    review = None
    if request.user.is_authenticated:
        review = request.user.reviews.filter(user=request.user)
    if review:
        review_form = ReviewForm(instance=review[0])
    else:
        review_form = ReviewForm()
    return render(request, 'recipe/recipe_detail.html',
                  {'recipe': Recipe.objects.get(slug=slug),
                   'review_form': review_form,
                   'reviews': Recipe.objects.get(slug=slug).reviews.order_by('-publish_date'),
                   'slug': slug})


@login_required
@require_POST
def review(request: HttpRequest, slug):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = request.user.reviews.filter(user=request.user)
        if review:
            review = review[0]
        else:
            review = Review()
        review.user = request.user
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
