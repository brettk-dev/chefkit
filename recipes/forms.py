from django import forms
from django.forms import Form, ModelForm, inlineformset_factory

from .models import Ingredient, Recipe, Step


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'serves', 'time', 'description')


class IngredientForm(ModelForm):
    unit = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Ingredient
        fields = ('quantity', 'unit', 'name')


class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ('number', 'description')


IngredientInlineFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1)

StepInlineFormSet = inlineformset_factory(
    Recipe, Step, form=StepForm, extra=1)
