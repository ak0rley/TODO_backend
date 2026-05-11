# serializers.py converts python objects to JSON format and vice versa, which is essential for API communication.

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at'
        ]