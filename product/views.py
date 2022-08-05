from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('recipes:list')
    return render(request, 'product/index.html')
