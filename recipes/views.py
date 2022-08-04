from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import IngredientInlineFormSet, RecipeForm, StepInlineFormSet
from .models import Recipe


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_forms'] = IngredientInlineFormSet(
            self.request.POST or None)
        context['step_forms'] = StepInlineFormSet(
            self.request.POST or None)
        context['verb'] = 'Create'
        return context

    def form_valid(self, form, ingredient_forms, step_forms):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        ingredients = ingredient_forms.save(commit=False)
        for ingredient in ingredients:
            ingredient.recipe = self.object
            ingredient.save()
        steps = step_forms.save(commit=False)
        for step in steps:
            step.recipe = self.object
            step.save()
        return redirect('recipes:detail', pk=self.object.pk)

    def form_invalid(self, form, ingredient_forms, step_forms):
        return self.render_to_response(
            self.get_context_data(form=form, ingredient_forms=ingredient_forms, step_forms=step_forms))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_forms = IngredientInlineFormSet(request.POST)
        step_forms = StepInlineFormSet(request.POST)
        if form.is_valid() and ingredient_forms.is_valid() and step_forms.is_valid():
            return self.form_valid(form, ingredient_forms, step_forms)
        else:
            return self.form_invalid(form, ingredient_forms, step_forms)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_forms'] = IngredientInlineFormSet(
            self.request.POST or None, instance=self.object)
        context['step_forms'] = StepInlineFormSet(
            self.request.POST or None, instance=self.object)
        context['verb'] = 'Update'
        return context

    def form_valid(self, form, ingredient_forms, step_forms):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        ingredients = ingredient_forms.save(commit=False)
        for ingredient in ingredients:
            ingredient.recipe = self.object
            ingredient.save()
        for ingredient in ingredient_forms.deleted_objects:
            ingredient.delete()
        steps = step_forms.save(commit=False)
        for step in steps:
            step.recipe = self.object
            step.save()
        for step in step_forms.deleted_objects:
            step.delete()
        return redirect('recipes:detail', pk=self.object.pk)

    def form_invalid(self, form, ingredient_forms, step_forms):
        return self.render_to_response(
            self.get_context_data(form=form, ingredient_forms=ingredient_forms, step_forms=step_forms))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_forms = IngredientInlineFormSet(
            request.POST, instance=self.object)
        step_forms = StepInlineFormSet(request.POST, instance=self.object)
        if form.is_valid() and ingredient_forms.is_valid() and step_forms.is_valid():
            return self.form_valid(form, ingredient_forms, step_forms)
        else:
            return self.form_invalid(form, ingredient_forms, step_forms)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:list')
