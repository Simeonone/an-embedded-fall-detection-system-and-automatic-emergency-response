from django.urls import path
from . import views

urlpatterns = [
    path('fall-detection-data/', views.FallDetectionDataCreateView.as_view(), name='fall-detection-data-create'),
    path('fall-detection-data/list/', views.FallDetectionDataListView.as_view(), name='fall-detection-data-list'),
]