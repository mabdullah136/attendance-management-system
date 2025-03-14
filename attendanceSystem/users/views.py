from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from users import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken,TokenError
from django.conf import settings
from django.utils.timezone import now,timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.settings import api_settings

# Create your views here.
class UserCreateView(APIView):
    serializer_class = serializers.UserCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'User created successfully',
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
        
class UserLoginView(APIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        # refresh["role"] = user.role
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                    'is_active': user.is_active,
                    'first_name': user.first_name,
                    'user_id': user.id,
                },
            },
            status=status.HTTP_200_OK,
        )

        response.data['access_token'] = access_token

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=settings.SECURE_COOKIE,  # Adjust this flag based on your environment (True/False)
            samesite='Lax',  # Adjust as per your requirement (Lax/Strict/None)
            expires=now() + timedelta(days=7), 
        )

        return response
    
class UserLogoutView(APIView):
    def post(self, request):
        response = Response(
            {
                'status': 'success',
                'message': 'Logout successful',
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie('refresh_token')

        return response
    
class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token not found in cookies'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode Token
            refresh = RefreshToken(refresh_token)
            
            user_id = refresh[api_settings.USER_ID_CLAIM]
            
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

            access_token = str(refresh.access_token)

            return Response(
                {
                    'status': 'success',
                    'message': 'Access token refreshed successfully',
                    'data': {
                        'email': user.email,
                        'username': user.username,
                        'user_id': user.id,
                    },
                    'access_token': access_token,
                },
                status=status.HTTP_200_OK,
            )

        except TokenError as e:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserUpdateView(APIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated] 

    def put(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('bearer '):
            return Response(
                {'error': 'Authorization token missing or invalid'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(' ')[1]

        try:
            # Decode the token to extract user ID
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']

            # Find the user by ID
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Update the user with the data from the request
            serializer = self.serializer_class(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'User updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        except ValidationError as ve:
        # Return serializer validation errors
            return Response({'errors': ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': 'Invalid token or insufficient permissions'},
                status=status.HTTP_401_UNAUTHORIZED
            )