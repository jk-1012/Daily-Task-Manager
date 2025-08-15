from rest_framework import serializers
from .models import Task
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = ['id','owner','title','description','due_date','priority','category','reminder','completed','created_at']
