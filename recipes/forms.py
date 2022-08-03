from django.forms import Form, ModelForm, inlineformset_factory

from .models import Ingredient, Recipe, Step


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'time')


IngredientInlineFormSet = inlineformset_factory(
    Recipe, Ingredient, fields=('quantity', 'unit', 'name'), extra=1)

StepInlineFormSet = inlineformset_factory(
    Recipe, Step, fields=('number', 'description'), extra=1)
