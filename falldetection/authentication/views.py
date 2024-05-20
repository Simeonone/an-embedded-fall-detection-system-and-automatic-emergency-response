from django.shortcuts import render, redirect
from user_registration.models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except User.DoesNotExist:
            error_message = 'Invalid email or password'
            return render(request, 'authentication/login.html', {'error_message': error_message})
    
    return render(request, 'authentication/login.html')


def dashboard_view(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        user = User.objects.get(id=user_id)
        device_connected = False  # Dummy value, update later
        return render(request, 'authentication/dashboard.html', {'user': user, 'device_connected': device_connected})
    else:
        return redirect('login')