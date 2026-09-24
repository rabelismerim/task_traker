from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # <--- Adicionado como ReadOnlyField

    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("A data de vencimento não pode ser uma data no passado.")
        return value