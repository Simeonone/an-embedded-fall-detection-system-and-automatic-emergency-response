from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from user_registration.models import User, EmergencyContact
from django.http import JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import FallDetection
from django.http import HttpResponse
import requests
import io
import base64
from django.http import StreamingHttpResponse
from django_twilio.client import twilio_client
from twilio.rest import Client
import os
from django.db import IntegrityError
from user_registration.forms import UserRegistrationForm
from django.urls import reverse
import json

# import matplotlib
# matplotlib.use('Agg') set the backend to Agg
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# from django.http import JsonResponse
# import subprocess

# def fall_detection_view(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         timestamp = request.POST.get('timestamp')
#         accelerometer_data = request.POST.get('accelerometer_data')

#         try:
#             user = User.objects.get(id=user_id)
#             fall_detection = FallDetection(
#                 user=user,
#                 timestamp=timestamp,
#                 accelerometer_data=accelerometer_data
#             )
#             fall_detection.save()
#             return JsonResponse({'message': 'Fall detection data saved successfully'})
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# def fall_detection_view(request):
#     if request.method == 'POST':
#         fall_data = request.POST.dict()
        
#         # Retrieve all fall detection data from the database
#         fall_events = FallDetection.objects.all().order_by('-timestamp')


#         # Generate the PDF
#         html_string = render_to_string('authentication/fall_detection_pdf.html', {'fall_data': fall_data})
#         html = HTML(string=html_string)
#         pdf_file = html.write_pdf()
        
#         # Save the PDF file or store it in the database
#         # ...
        
#         return JsonResponse({'status': 'success'})
    
#     return JsonResponse({'status': 'error'})

def fall_detection_view(request):
    # Make a GET request to the fall detection data API
    response = requests.get('http://localhost:8000/api/fall-detection-data/list/')
    fall_data = response.json()
    
    # Generate the line chart using Matplotlib
    import matplotlib
    matplotlib.use('Agg')  # Set the backend to Agg
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    timestamps = [fall_event['timestamp'] for fall_event in fall_data]
    accel_x = [fall_event['accel_x'] for fall_event in fall_data]
    accel_y = [fall_event['accel_y'] for fall_event in fall_data]
    accel_z = [fall_event['accel_z'] for fall_event in fall_data]

    ax.plot(timestamps, accel_x, label='Accelerometer X')
    ax.plot(timestamps, accel_y, label='Accelerometer Y')
    ax.plot(timestamps, accel_z, label='Accelerometer Z')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45)
    ax.legend()
    ax.set_title('Accelerometer Data')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Acceleration')
    ax.grid(True)

    # Save the chart to a bytes buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the chart image to base64
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)



    # Generate the PDF
    html_string = render_to_string('authentication/fall_detection_pdf.html', {'fall_data': fall_data, 'chart_data':chart_data})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    
    # Create an HTTP response with the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="fall_detection_report.pdf"'
    response.write(pdf_file)
    
    return response

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
        emergency_contacts = EmergencyContact.objects.filter(user=user)
        device_connected = False  # Dummy value, update later
        latest_fall_detection = FallDetection.objects.order_by('-timestamp').first()
        
        if request.method == 'POST':
            # Fall detection message received
            def event_stream():
                yield 'data: Fall detected!\n\n'
            
            response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            return response
        
        return render(request, 'authentication/dashboard.html', 
                      {
                          'user': user,
                          'emergency_contacts': emergency_contacts,
                          'device_connected': device_connected,
                          'latest_fall_detection': latest_fall_detection
                      })
    else:
        return redirect('login')
def get_emergency_contacts(user):
    emergency_contacts = user.emergency_contacts.all()
    return emergency_contacts

def logout_view(request):
    # Clear the user session and redirect to the login page
    request.session.flush()
    return redirect('login')

def get_twilio_client():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    return Client(account_sid, auth_token)


def send_emergency_sms(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)

        # Parse JSON data from request body
        data = json.loads(request.body)
        location = data.get('location')

        # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        emergency_contacts = user.emergency_contacts.all()
        client = get_twilio_client()
        

        # Get the current location
        # location = request.POST.get('location')

        # Generate the fall detection PDF link
        fall_detection_pdf_link = request.build_absolute_uri(reverse('fall_detection_pdf'))

        
        for contact in emergency_contacts:
            message_body = f"ALERT!!\n\nEmergency SOS triggered for {user.full_name}.\n\n"
            message_body += f"Phone Number: {user.phone_number}\n"
            message_body += f"Blood Group: {user.blood_group}\n"
            message_body += f"Fall Detection report in PDF: {fall_detection_pdf_link}\n"
            if location:
                message_body += f"Current Location: {location}\n"
            else:
                message_body += "Current Location: Not available\n"
            message_body += "Please check on them immediately."

            message = client.messages.create(
                body=message_body,
                from_=twilio_phone_number,
                to=contact.phone
            )
            print(f"SMS sent to {contact.phone}. Message SID: {message.sid}")

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'})