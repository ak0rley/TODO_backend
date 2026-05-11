from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo


class TodoModelTest(TestCase):
    """Test the Todo model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_todo_creation(self):
        """Test creating a Todo instance"""
        todo = Todo.objects.create(
            title='Test Todo',
            description='Test description',
            owner=self.user
        )
        self.assertEqual(todo.title, 'Test Todo')
        self.assertEqual(todo.description, 'Test description')
        self.assertFalse(todo.completed)
        self.assertEqual(todo.owner, self.user)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)

    def test_todo_str_method(self):
        """Test the string representation of Todo"""
        todo = Todo.objects.create(
            title='Test Todo',
            owner=self.user
        )
        self.assertEqual(str(todo), 'Test Todo')

    def test_todo_ordering(self):
        """Test that todos are ordered by created_at descending"""
        todo1 = Todo.objects.create(title='First Todo', owner=self.user)
        todo2 = Todo.objects.create(title='Second Todo', owner=self.user)

        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo2)  # Most recent first
        self.assertEqual(todos[1], todo1)


class TodoAPITest(APITestCase):
    """Test the Todo API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.todo_data = {
            'title': 'Test Todo',
            'description': 'Test description',
            'completed': False
        }

    def test_create_todo_authenticated(self):
        """Test creating a todo when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('todo-list')
        response = self.client.post(url, self.todo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, 'Test Todo')
        self.assertEqual(Todo.objects.get().owner, self.user)

    def test_create_todo_unauthenticated(self):
        """Test creating a todo when not authenticated"""
        url = reverse('todo-list')
        response = self.client.post(url, self.todo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Todo.objects.count(), 0)

    def test_list_todos_authenticated(self):
        """Test listing todos for authenticated user"""
        # Create todos for both users
        Todo.objects.create(title='User Todo', owner=self.user)
        Todo.objects.create(title='Other User Todo', owner=self.other_user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only user's todo
        self.assertEqual(response.data[0]['title'], 'User Todo')

    def test_list_todos_unauthenticated(self):
        """Test listing todos when not authenticated"""
        url = reverse('todo-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_todo_own(self):
        """Test retrieving own todo"""
        todo = Todo.objects.create(title='My Todo', owner=self.user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'My Todo')

    def test_retrieve_todo_other_user(self):
        """Test retrieving another user's todo (should fail)"""
        todo = Todo.objects.create(title='Other Todo', owner=self.other_user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo_own(self):
        """Test updating own todo"""
        todo = Todo.objects.create(title='Old Title', owner=self.user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        update_data = {'title': 'New Title', 'completed': True}
        response = self.client.put(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'New Title')
        self.assertTrue(todo.completed)

    def test_update_todo_other_user(self):
        """Test updating another user's todo (should fail)"""
        todo = Todo.objects.create(title='Other Todo', owner=self.other_user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        update_data = {'title': 'Hacked Title'}
        response = self.client.put(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_own(self):
        """Test deleting own todo"""
        todo = Todo.objects.create(title='Todo to Delete', owner=self.user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_todo_other_user(self):
        """Test deleting another user's todo (should fail)"""
        todo = Todo.objects.create(title='Other Todo', owner=self.other_user)

        self.client.force_authenticate(user=self.user)
        url = reverse('todo-detail', kwargs={'pk': todo.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Todo.objects.count(), 1)  # Todo still exists
