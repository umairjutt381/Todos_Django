
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    # path('profile/', views.user_profile, name='user_profile'),
    path('context/', views.show_context, name='show_context'),
    path('todos/', views.todo_list, name='todo_list'),
    path('createtodo/', views.create_todo, name='create_todo'),
    path('updatetodo/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('deletetodo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]

