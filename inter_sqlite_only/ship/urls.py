from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    TaskViewSet,
    register_view, login_view, logout_view, current_user,
    login_page, register_page, dashboard_page, tasks_page, profile_page
)

router = DefaultRouter()
router.register(r'api/tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Auth API
    path('api/auth/register/', register_view),
    path('api/auth/login/', login_view),
    path('api/auth/logout/', logout_view),
    path('api/auth/user/', current_user),

    # Pages
    path('login/', login_page, name='login'),
    path('', login_page),                      # default landing = login page
    path('register/', register_page),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('tasks-page/', tasks_page),
    path('profile/', profile_page),

    # Tasks API (DRF)
    path('', include(router.urls)),

    path('logout/', views.logout_view, name='logout'),
]
