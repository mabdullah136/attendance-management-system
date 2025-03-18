from rest_framework import serializers
from .models import Holiday
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError

class HolidayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'title', 'from_date', 'to_date', 'description', 'created_by', 'created_at']  # Include all fields

    def validate(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        if isinstance(from_date, str) and from_date:
            from_date = parse_date(from_date)
            if from_date is None:
                raise ValidationError("Invalid date format for from-date.")
            data["from_date"] = from_date

        if isinstance(to_date, str) and to_date:
            to_date = parse_date(to_date)
            if to_date is None:
                raise ValidationError("Invalid date format for to-date.")
            data["to_date"] = to_date

        if from_date and to_date and from_date > to_date:
            raise ValidationError("from_date cannot be after to_date.")

        return data  # ✅ You forgot this!

    def create(self, validated_data):
        return Holiday.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.from_date = validated_data.get('from_date', instance.from_date)
        instance.to_date = validated_data.get('to_date', instance.to_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

class HolidayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'title', 'from_date', 'to_date', 'description', 'created_by', 'created_at']  # Include all fields
        
    