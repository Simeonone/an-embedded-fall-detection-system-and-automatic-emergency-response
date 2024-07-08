from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FallDetectionData
from .serializers import FallDetectionDataSerializer

class FallDetectionDataCreateView(generics.CreateAPIView):
    queryset = FallDetectionData.objects.all()
    serializer_class = FallDetectionDataSerializer

    def get(self, request, *args, **kwargs):
       # Return a simple response for GET requests
       return Response({"message": "Use POST to create new fall detection data"}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class FallDetectionDataListView(generics.ListAPIView):
    queryset = FallDetectionData.objects.all()
    serializer_class = FallDetectionDataSerializer

# @api_view(['GET','POST'])
# def fall_detection_data(request):
#     if request.method == 'GET':
#         fall_data = FallDetectionData.objects.all()
#         serializer = FallDetectionDataSerializer(fall_data, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = FallDetectionDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response({'message': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'POST':
#         data = request.data
        
#         try:
#             # Extract the relevant data from the request
#             dsp_time = data.get('dsp_time', 0)
#             classification_time = data.get('classification_time', 0)
#             anomaly_time = data.get('anomaly_time', 0)
#             predicted_activity = data.get('predicted_activity', '')
#             accel_x = data.get('accel_x', 0.0)
#             accel_y = data.get('accel_y', 0.0)
#             accel_z = data.get('accel_z', 0.0)
#             counts = data.get('counts', [0, 0, 0, 0])
            
#             # Extract the counts from the counts array, handling null values
#             stand_count = counts[0] if counts[0] is not None else 0
#             uncertain_count = counts[1] if counts[1] is not None else 0
#             fall_count = counts[2] if counts[2] is not None else 0
#             other_count = counts[3] if counts[3] is not None else 0
            
#             # Create a new FallDetectionData instance and save it to the database
#             fall_data = FallDetectionData(
#                 dsp_time=dsp_time,
#                 classification_time=classification_time,
#                 anomaly_time=anomaly_time,
#                 predicted_activity=predicted_activity,
#                 accel_x=accel_x,
#                 accel_y=accel_y,
#                 accel_z=accel_z,
#                 stand_count=stand_count,
#                 uncertain_count=uncertain_count,
#                 fall_count=fall_count,
#                 other_count=other_count
#             )
#             fall_data.save()
            
#             return Response({'message': 'Fall detection data received and saved.'}, status=status.HTTP_201_CREATED)
        
#         except Exception as e:
#             # Handle any exceptions
#             error_message = str(e)
#             print(f"Error occurred while processing fall detection data: {error_message}")
#             return Response({'error': 'An error occurred while processing the data.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response({'message': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)