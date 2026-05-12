#from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all tasks",
        description="Returns all tasks.",
        responses={
            200: {
                "type": "object",
                "example": {
                    "message": "These are today's tasks",
                    "tasks": [
                        {
                            "id": 1,
                            "title": "Complete the assignment",
                            "completed": False
                        }
                    ]
                }
            }
        }
    )
    def list(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)

        return Response({
            "message": "These are today's tasks",
            "tasks": serializer.data
        })


class HelloView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Hello endpoint",
        description="Returns a welcome message.",
        responses={200: dict}
    )
    def get(self, request):
        return Response({"message": "Hello World"})