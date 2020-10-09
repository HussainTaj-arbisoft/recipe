from django.contrib import admin
from .models import *
from .forms import RecipeForm


class IngredientInline(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author',
                    'prep_time', 'image_url', 'tags')
    list_filter = ('title',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'pub_date'
    ordering = ('pub_date',)

    form = RecipeForm

    inlines = [
        IngredientInline
    ]


# admin.site.register(Ingredient)
admin.site.register(Review)
