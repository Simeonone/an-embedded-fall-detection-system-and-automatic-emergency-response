from django import forms

class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = forms.CharField(max_length=10)
    home_address = forms.CharField(max_length=200)
    emergency_contacts = forms.IntegerField(min_value=1, max_value=3)
    password = forms.CharField(widget=forms.PasswordInput)