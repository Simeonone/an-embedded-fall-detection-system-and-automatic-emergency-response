from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import UserRegistrationForm
from .models import User, EmergencyContact

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
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

                num_contacts = int(request.POST.get('emergency_contacts', 0))
                for i in range(1, num_contacts + 1):
                    name = request.POST.get(f'contact_{i}_name')
                    relationship = request.POST.get(f'contact_{i}_relationship')
                    phone = request.POST.get(f'contact_{i}_phone')
                    if name and relationship and phone:
                        EmergencyContact.objects.create(user=user, name=name, relationship=relationship, phone=phone)

                return redirect('login')

            except IntegrityError:
                form.add_error('email', 'An account with this email already exists.')

    else:
        form = UserRegistrationForm()

    return render(request, 'user_registration/user_registration.html', {'form': form})