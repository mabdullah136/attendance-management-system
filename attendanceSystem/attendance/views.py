from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from attendance import serializers
from .models import Attendance
from .permissions import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated

class AttendanceCreateView(APIView):
    serializer_class = serializers.AttendanceCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]  # 🔹 Enforce token & role check

    def post(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id  # 🔹 Assign logged-in user automatically
            serializer = self.serializer_class(data=request.data)
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
            return Response(
                {'error': 'An unexpected error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
