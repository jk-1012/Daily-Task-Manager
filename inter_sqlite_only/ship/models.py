from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Task(models.Model):
    PRIORITY_CHOICES = [('low','Low'),('medium','Medium'),('high','High')]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=80, blank=True, default='General')
    reminder = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
