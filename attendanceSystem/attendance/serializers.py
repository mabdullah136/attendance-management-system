from rest_framework import serializers
from .models import Attendance
from rest_framework.exceptions import ValidationError

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'check_in', 'check_out', 'status', 'created_at']

    def validate(self, data):
        user = data.get('user')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        # Ensure the user does not have an active attendance without checkout
        existing_attendance = Attendance.objects.filter(user=user, check_out__isnull=True).exists()
        
        if check_in and existing_attendance:
            raise ValidationError("User already has an active attendance without check-out.")

        if check_out and not check_in:
            last_attendance = Attendance.objects.filter(user=user, check_out__isnull=True).first()
            if not last_attendance:
                raise ValidationError("Cannot check out without checking in first.")

        return data

    def create(self, validated_data):
        return Attendance.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Allow check-out update while keeping check-in unchanged."""
        instance.check_out = validated_data.get('check_out', instance.check_out)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
