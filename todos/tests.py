from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoModelTests(TestCase):
    def test_todo_creation(self):
        """Test that a Todo is created correctly."""
        todo = Todo.objects.create(title="Test Todo", description="Test Description")
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertFalse(todo.is_resolved)
        self.assertEqual(str(todo), "Test Todo")

class TodoViewTests(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="Test Todo")

    def test_todo_list_view(self):
        """Test that the list view returns 200 and contains the todo."""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_todo_create_view(self):
        """Test creating a new todo via the view."""
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': ''
        })
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view(self):
        """Test updating an existing todo."""
        response = self.client.post(reverse('todo_update', args=[self.todo.pk]), {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'due_date': ''
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_todo_delete_view(self):
        """Test deleting a todo."""
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())

    def test_todo_resolve_action(self):
        """Test marking a todo as resolved."""
        response = self.client.post(reverse('todo_resolve', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
