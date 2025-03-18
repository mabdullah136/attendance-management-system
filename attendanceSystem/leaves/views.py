from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from leaves import serializers
from .models import LeaveRequest
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Q

# Create your views here.

class LeaveRequestView(APIView):
    serializer_class = serializers.LeaveRequestCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()  # ✅ Make a mutable copy
            print(request.user.id)
            mutable_data['user'] = request.user.id 

            serializer = self.serializer_class(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            leave_request = serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'Leave request created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as ve:
            return Response(
                {'errors': ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error: {e}") 
            return Response(
                {'error': 'An unexpected error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                leave_request = LeaveRequest.objects.get(id=id, user=request.user)
                serializer = self.serializer_class(leave_request)
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            except LeaveRequest.DoesNotExist:
                return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)

        leave_requests = LeaveRequest.objects.filter(user=request.user)
        serializer = self.serializer_class(leave_requests, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)