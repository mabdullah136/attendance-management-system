from rest_framework import serializers
from .models import LeaveRequest
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError

class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id','user', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by', 'created_at']
        
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if isinstance(start_date, str) and start_date:
            start_date = parse_date(start_date)
            if start_date is None:
                raise ValidationError("Invalid date format for start-date.")
            data["start_date"] = start_date

        if isinstance(end_date, str) and end_date:
            end_date = parse_date(end_date)
            if end_date is None:
                raise ValidationError("Invalid date format for end-date.")
            data["end_date"] = end_date

        if start_date and end_date and start_date > end_date:
            raise ValidationError("start_date cannot be after end_date.")

        return data
    
    def create(self, validated_data):
        return LeaveRequest.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.leave_type = validated_data.get('leave_type', instance.leave_type)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.save()
        return instance