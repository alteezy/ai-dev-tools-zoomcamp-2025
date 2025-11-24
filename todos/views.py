from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoListView(ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_todos'] = Todo.objects.filter(is_resolved=False).order_by('due_date')
        context['resolved_todos'] = Todo.objects.filter(is_resolved=True).order_by('-created_at')
        return context

class TodoCreateView(CreateView):
    model = Todo
    fields = ['title', 'description', 'due_date']
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')

class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['title', 'description', 'due_date']
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

def resolve_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.is_resolved = not todo.is_resolved
        todo.save()
    return redirect('todo_list')
