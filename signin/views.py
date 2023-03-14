from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == '' and password == '':
            messages.error(request, "Username and password can't be blank")
            return redirect('signin')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:

                return redirect('dashboard')
            else:
                return redirect('home')

        else:
            messages.error(request, 'Wrong username or password')

    return render(request, 'signin.html')
