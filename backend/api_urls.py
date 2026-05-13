from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    AuthViewSet,
    UserViewSet,
    TodoViewSet,
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'todos', TodoViewSet, basename='todos')

urlpatterns = [
    path('', include(router.urls)),
]

