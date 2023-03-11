from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):

    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        password = request.POST['password']
        comf_password = request.POST['comf-password']

        if fullname == '' and username == '' and password == '':
            messages.error(request, "Fields can't be blank")
            return redirect('signup')

        if password != comf_password:
            messages.error(request, "Password dosen't match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = fullname
        user.save()
        messages.success(request, 'User created successfully')

    return render(request, 'signup.html')
