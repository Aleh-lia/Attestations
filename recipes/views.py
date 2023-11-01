from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def lunch(request):
    context = {
        'title': 'Обеды'
    }
    return render(request, 'recipes/lunch.html', context)

