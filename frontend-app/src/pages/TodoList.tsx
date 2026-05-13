import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import { todoService } from '../services/api';
import { Todo } from '../types';
import './Todos.css';

export const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await todoService.getTodos();
      setTodos(response.results || response);
    } catch (error) {
      console.error('Failed to fetch todos', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure?')) {
      try {
        await todoService.deleteTodo(id);
        setTodos(todos.filter((t) => t.id !== id));
      } catch (error) {
        console.error('Failed to delete todo', error);
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/register');
  };

  if (loading) return <div className="container"><p>Loading...</p></div>;

  return (
    <div className="container">
      <nav className="navbar">
        <h1>Todos | Todos</h1>
        <div className="nav-buttons">
          <span>Welcome, {user?.username}!</span>
          <button onClick={() => navigate('/todos/create')} className="btn-primary">
            Add New Todo
          </button>
          <button onClick={handleLogout} className="btn-danger">
            Logout
          </button>
        </div>
      </nav>

      <div className="todos-section">
        <h2>Your Todos</h2>
        {todos.length === 0 ? (
          <p>No todos yet. Create one to get started!</p>
        ) : (
          <div className="todos-grid">
            {todos.map((todo) => (
              <div key={todo.id} className="todo-card">
                <h3>{todo.task_name}</h3>
                <p className="description">{todo.description}</p>
                <p className="text">{todo.text}</p>
                <small className="date">
                  Created: {new Date(todo.created_at).toLocaleDateString()}
                </small>
                <div className="todo-actions">
                  <button onClick={() => navigate(`/todos/${todo.id}`)} className="btn-edit">
                    Edit
                  </button>
                  <button onClick={() => handleDelete(todo.id)} className="btn-delete">
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

