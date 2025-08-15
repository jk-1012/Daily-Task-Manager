from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth import logout

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on tasks.
    Only returns tasks for the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return tasks owned by the logged-in user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Assign the logged-in user as the task owner
        serializer.save(owner=self.request.user)


# ---------- PAGE VIEWS ----------

def login_page(request):
    # If the user is already authenticated, go straight to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'register.html')

@login_required(login_url='/login/')
def dashboard_page(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
def tasks_page(request):
    return render(request, 'tasks.html')

@login_required(login_url='/login/')
def profile_page(request):
    return render(request, 'profile.html')

# ---------- AUTH API ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    # Expecting: username, email (optional), password
    from django.contrib.auth.models import User
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '').strip()

    if not username or not password:
        return Response({'detail': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email or None, password=password)
    return Response({'detail': 'created'}, status=status.HTTP_201_CREATED)

@require_POST
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'detail': 'logged out'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    u = request.user
    return Response({
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name,
    })
