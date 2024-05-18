# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            # Redirect to a success page or login page
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/user_registration.html', {'form': form})