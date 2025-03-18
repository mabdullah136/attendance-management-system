from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from holiday import serializers
from .models import Holiday
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Q

class HolidayCreateView(APIView):
    serializer_class = serializers.HolidayCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()  # ✅ Make a mutable copy
            mutable_data['created_by'] = request.user.id 

            serializer = self.serializer_class(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            holiday = serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'Holiday created successfully',
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
    
class HolidayListView(APIView):
    serializer_class = serializers.HolidayListSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        today = now().date()

        holidays = Holiday.objects.filter(
            Q(from_date__gte=today) | Q(to_date__gte=today)
        )
        serializer = self.serializer_class(holidays, many=True)
        return Response(
            {
                'status': 'success',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
