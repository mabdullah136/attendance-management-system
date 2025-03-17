from rest_framework import serializers
from .models import Attendance
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils.dateparse import parse_datetime

class AttendanceCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'check_in', 'check_out', 'status', 'created_at', 'id']

    def validate(self, data):
        user = data.get('user')
        check_in = data.get('check_in')

        if isinstance(check_in, str) and check_in:
            check_in = parse_datetime(check_in)
            if check_in is None:
                raise ValidationError("Invalid datetime format for check-in.")
            data["check_in"] = check_in  

        existing_attendance = Attendance.objects.filter(user=user, check_out__isnull=True).exists()
        if check_in and existing_attendance:
            raise ValidationError("User already has an active attendance without check-out.")

        return data

    def create(self, validated_data):
        if not validated_data.get("check_in"):
            raise ValidationError("Check-in time is required to create attendance.")
        
        return Attendance.objects.create(**validated_data)
    
class AttendanceCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'check_in', 'check_out', 'status', 'created_at', 'id']
        

    def validate(self, data):
        check_out = data.get('check_out')

        if isinstance(check_out, str) and check_out:
            check_out = parse_datetime(check_out)
            if check_out is None:
                raise ValidationError("Invalid datetime format for check-out.")
            data["check_out"] = check_out  

        return data

    def update(self, instance, validated_data):
        if not validated_data.get("check_out"):
            raise ValidationError("Check-out time is required to update attendance.")
        
        instance.check_out = validated_data.get("check_out")
        instance.status = "CHECK_OUT"
        instance.save()
        return instance
