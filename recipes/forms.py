from django.forms import Form, inlineformset_factory

from .models import Ingredient, Recipe, Step

IngredientInlineFormSet = inlineformset_factory(
    Recipe, Ingredient, fields=('qty', 'unit', 'name'), extra=1)

StepInlineFormSet = inlineformset_factory(
    Recipe, Step, fields=('step_number', 'description'), extra=1)
