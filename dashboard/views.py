from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.cache import cache_control


def show_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users_data = User.objects.all()
            return render(request, 'dashboard.html', {'users': users_data})
        else:
            return redirect('home')
    else:
        return redirect('login')


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('dashboard')


def edit_user(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user-edit.html', {'user': user})


def update_user(request, id):

    if request.method == 'POST':

        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if fullname == '' and username == '' and password == '':
            messages.error(request, "Fields can't be blank")
            return redirect('edit', id=id)

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('edit', id=id)

        user = User.objects.get(id=id)
        user.first_name = fullname
        user.username = username
        user.email = email
        user.password = password
        user.save()
        messages.success(request, 'User updated successfully')
        return redirect('dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_user(request):

    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        comf_password = request.POST['comf-password']
        is_super = request.POST['is_superuser']

        if fullname == '' and username == '' and password == '':
            messages.error(request, "Fields can't be blank")
            return redirect('create')

        if password != comf_password:
            messages.error(request, "Password dosen't match")
            return redirect('create')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('create')

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('create')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = fullname
        user.email = email

        if is_super == 'checked':
            user.is_superuser = True

        user.save()
        messages.success(request, 'User created successfully')
        return redirect('dashboard')

    return render(request, 'new-user.html')
