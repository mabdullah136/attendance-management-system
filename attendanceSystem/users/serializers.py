from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError('Username already exists')
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        validated_data['first_name'] = validated_data.get('first_name', validated_data.get('username', ''))
        user = CustomUser.objects.create_user(**validated_data)  # Use `create_user` for password hashing
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError('Invalid email or password.')

        if not user.check_password(password):
            raise ValidationError('Invalid email or password.')

        if not user.is_active:
            raise ValidationError('This account is inactive.')

        data['user'] = user
        return data
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'is_active']
        extra_kwargs = {
            'email': {'read_only': True},
            'username': {'read_only': True},
            'role': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            new_username = validated_data['username']
            if new_username != instance.username:
                if CustomUser.objects.filter(username=new_username).exists():
                    raise ValidationError({'username': 'This username is already taken.'})
                instance.username = new_username

        for field in ['phone', 'first_name', 'last_name']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance
