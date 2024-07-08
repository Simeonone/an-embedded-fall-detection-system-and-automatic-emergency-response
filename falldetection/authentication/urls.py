from django.urls import path
from . import views
from .views import send_emergency_sms

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('fall-detection-pdf/', views.fall_detection_view, name='fall_detection_pdf'),
    path('send-emergency-sms/', send_emergency_sms, name='send_emergency_sms'),
]