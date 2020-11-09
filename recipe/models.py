from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import fields
from django.urls import reverse
from taggit.managers import TaggableManager


class Recipe(models.Model):
    title = fields.CharField(max_length=200)
    slug = fields.SlugField(unique=True, unique_for_date='pub_date')
    instructions = fields.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True,
                               related_name='recipes')

    prep_time = fields.DurationField()
    pub_date = fields.DateTimeField(auto_now_add=True)
    image_url = fields.URLField()

    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe:recipe", kwargs={"slug": self.slug})


class Ingredient(models.Model):
    name = fields.CharField(max_length=125)
    amount = fields.DecimalField(max_digits=4, decimal_places=2, validators=[
        MinValueValidator(0, 'Value cannot be negative.')
    ])
    UNIT_CHOICES = [
        ('tb-sp', 'Table Spoon'), ('t-sp', 'Tea Spoon'),
        ('cup', 'Cup'), ('lt', 'Litre'), ('kg', 'Kilogram'),
        ('gm', 'gram')
    ]
    unit = fields.CharField(choices=UNIT_CHOICES, max_length=10)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = fields.SmallIntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)],
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        default=5)
    comment = fields.CharField(max_length=255)
    publish_date = fields.DateTimeField(auto_now_add=True)
    updated_date = fields.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='reviews')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='reviews')

    def __str__(self):
        return f'{self.rating} {self.comment[:20]}'

    class Meta:
        ordering = ('-publish_date',)
