import markdown as md
from django import template
from django.db.models import Avg
from django.utils.safestring import mark_safe

from recipe.models import Review

register = template.Library()


@register.filter(name='duration')
def duration_format(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f'{hours:02}:{minutes:02}'


@register.simple_tag(name='average_rating')
def get_average_rating(slug):
    avg = (
        Review.objects.filter(recipe__slug=slug)
        .aggregate(Avg('rating'))
        ['rating__avg'])
    if avg:
        return round(avg, 1)
    return 'New'


@register.filter(name='markdown')
def markdown_format(data):
    return mark_safe(md.markdown(data))
