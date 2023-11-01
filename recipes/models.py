from django.db import models

# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    steps = models.CharField(max_length=200)
    time = models.TimeField()
    image = models.ImageField()
    author = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=500)
    calories = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=100)


class RecipesCategory(models.Model):
    recipes_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)