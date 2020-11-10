from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import (HttpRequest, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView
from taggit.models import Tag

from account.models import User
from recipe.forms import RecipeForm, RecipeIngredientFormSet, ReviewForm
from recipe.models import Recipe, Review


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 12
    template_name = "recipe/recipe_list.html"


def recipe(request: HttpRequest, slug):
    review = None
    if request.user.is_authenticated:
        review = request.user.reviews.filter(user=request.user, recipe__slug=slug)
    if review:
        review_form = ReviewForm(instance=review[0])
    else:
        review_form = ReviewForm()
    return render(
        request,
        "recipe/recipe_detail.html",
        {
            "recipe": Recipe.objects.get(slug=slug),
            "review_form": review_form,
            "reviews": Recipe.objects.get(slug=slug).reviews.order_by("-publish_date"),
            "slug": slug,
        },
    )


@login_required
@require_POST
def review(request: HttpRequest, slug):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = request.user.reviews.filter(user=request.user, recipe__slug=slug)
        if review:
            review = review[0]
        else:
            review = Review()
        review.user = request.user
        review.comment = form.cleaned_data["comment"]
        review.rating = form.cleaned_data["rating"]
        review.recipe = Recipe.objects.get(slug=slug)
        review.save()
    return HttpResponseRedirect(review.recipe.get_absolute_url())


class TagRecipeListView(ListView):
    template_name = "recipe/recipe_list.html"
    paginate_by = 12

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = Recipe.objects.filter(tags__in=[tag])
        return queryset


class SearchRecipeListView(ListView):
    template_name = "recipe/recipe_list.html"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("query")
        queryset = Recipe.objects.filter(title__contains=query)
        return queryset


class UserRecipeListView(ListView):
    template_name = "recipe/user_recipe_list.html"
    paginate_by = 12

    def get_queryset(self):
        return Recipe.objects.filter(author__username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        return context


class RecipeCreateView(CreateView, LoginRequiredMixin):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipe/recipe_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["form_ingredients"] = RecipeIngredientFormSet(self.request.POST)
        else:
            context["form_ingredients"] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_ingredients = context["form_ingredients"]

        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        if form_ingredients.is_valid():
            form_ingredients.instance = self.object
            form_ingredients.save()
        return super(RecipeCreateView, self).form_valid(form)
