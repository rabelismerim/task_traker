from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate_due_date(self, value):
        """
        Valida se a data de vencimento não é anterior à data atual.
        Permite valores nulos/vazios se o campo for opcional.
        """
        if value is None:
            return value

        today = timezone.now().date()
        if value < today:
            raise serializers.ValidationError("A data de vencimento não pode ser anterior à data de hoje.")
        
        return value