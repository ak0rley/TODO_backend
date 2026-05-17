#from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        description="Returns all tasks."
    ),
    create=extend_schema(
        summary="Create a task",
        description="Creates a new task."
    ),
    retrieve=extend_schema(
        summary="Retrieve a task",
        description="Returns a single task by ID."
    ),
    update=extend_schema(
        summary="Update a task",
        description="Updates an existing task completely."
    ),
    partial_update=extend_schema(
        summary="Partially update a task",
        description="Updates part of a task."
    ),
    destroy=extend_schema(
        summary="Delete a task",
        description="Deletes a task."
    ),
)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

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
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        task = self.get_object()
        if task.user != self.request.user:       
            raise PermissionDenied("You can only edit your own tasks.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:   
            raise PermissionDenied("You can only delete your own tasks.")
        instance.delete()

    def list(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)

        return Response({
            "message": "These are today's tasks",
            "tasks": serializer.data
        })


class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Hello endpoint",
        description="Returns a welcome message.",
        responses={200: dict}
    )
    def get(self, request):
        return Response({"message": "Hello World"})