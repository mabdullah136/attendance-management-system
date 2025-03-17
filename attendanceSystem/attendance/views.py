from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from attendance import serializers
from .models import Attendance
from .permissions import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated

class AttendanceCheckInView(APIView):
    serializer_class = serializers.AttendanceCheckInSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] 

    def post(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()  # ✅ Make a mutable copy
            mutable_data['user'] = request.user.id 

            serializer = self.serializer_class(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            attendance = serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'Attendance created successfully',
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
            
class AttendanceCheckOutView(APIView):
    serializer_class = serializers.AttendanceCheckOutSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def put(self, request, attendance_id, *args, **kwargs):
        try:
            attendance = Attendance.objects.get(id=attendance_id, user=request.user)

            if attendance.check_out is not None:
                return Response(
                    {'error': 'This attendance entry is already checked out.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if attendance.check_in is None:
                return Response(
                    {'error': 'Cannot check out without a valid check-in.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.serializer_class(attendance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'Checked out successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        except Attendance.DoesNotExist:
            return Response(
                {'error': 'Attendance entry not found or does not belong to you.'},
                status=status.HTTP_404_NOT_FOUND
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

    

            
