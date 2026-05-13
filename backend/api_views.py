from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.middleware.csrf import get_token

from .models import Todo
from .serializers import (
    UserSerializer,
    TodoSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def csrf_token(self, request):
        """Get CSRF token"""
        token = get_token(request)
        return Response({'csrfToken': token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'message': 'User registered successfully!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login user"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # Create the session
                auth_login(request, user)
                return Response(
                    {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_admin': user.is_superuser,
                        'message': 'Login successful!'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid username or password!'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        auth_logout(request)
        return Response(
            {'message': 'Logout successful!'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user info"""
        user = request.user
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_superuser,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': 'Password changed successfully!'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User management endpoints"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        """Get all users (admin only)"""
        if not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can view all users'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class TodoViewSet(viewsets.ModelViewSet):
    """Todo management endpoints"""
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        """Return todos based on permissions"""
        user = self.request.user
        if user.is_superuser:
            return Todo.objects.all().order_by('-created_at')
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        """Create todo with current user"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Delete todo"""
        todo = self.get_object()
        
        # Check permissions
        if not request.user.is_superuser and todo.user != request.user:
            return Response(
                {'error': 'You do not have permission to delete this todo.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        todo.delete()
        return Response(
            {'message': 'Todo deleted successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        """Update todo"""
        todo = self.get_object()
        
        # Check permissions
        if not request.user.is_superuser and todo.user != request.user:
            return Response(
                {'error': 'You do not have permission to edit this todo.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

