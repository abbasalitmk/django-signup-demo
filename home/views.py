from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return render(request, 'home.html')
    else:
        return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    logout(request)
    return redirect('signin')
