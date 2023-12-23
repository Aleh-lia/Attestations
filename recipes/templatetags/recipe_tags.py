from django import template
from django.db.models import Count

from recipes import views
from recipes.models import *
from recipes.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('recipes/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    # cats = views.cats_db

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('recipes/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
