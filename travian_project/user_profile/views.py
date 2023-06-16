from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect

User = get_user_model()

@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'In order to sign up, you need to logout first')
        return redirect('base')
    if request.method == "POST":
        error = False
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not username or len(username) < 3 or User.objects.filter(username=username).exists():
            error = True
            messages.error(request, 'Username is too short or already exists.')
        if not email or len(email) < 3 or User.objects.filter(email=email).exists():
            error = True
            messages.error(request, 'Email is invalid or user with this email already exists.')
        if not password or not password_confirm or password != password_confirm or len(password) < 8:
            error = True
            messages.error(request, "Password must be at least 8 characters long and match.")
        if not error:
            user = User.objects.create(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            messages.success(request, "User registration successful!")
            return redirect('login')
    return render(request, 'registration/signup.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')  # Replace 'home' with the desired URL name for the home page
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'registration/login.html', context)
