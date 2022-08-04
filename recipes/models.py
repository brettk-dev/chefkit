from django.conf import settings
from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.IntegerField(default=0)
    serves = models.IntegerField(default=0)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.number}: {self.description}"
