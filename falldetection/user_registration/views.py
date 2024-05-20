# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            user = User(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                blood_group=form.cleaned_data['blood_group'],
                home_address=form.cleaned_data['home_address'],
                password=form.cleaned_data['password']
            )
            user.save()
            # Redirect to a success page or login page
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/user_registration.html', {'form': form})