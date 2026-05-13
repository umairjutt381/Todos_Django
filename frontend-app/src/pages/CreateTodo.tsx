import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { todoService } from '../services/api';
import { Todo } from '../types';
import './CreateTodo.css';

export const CreateUpdateTodo: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task_name, setTaskName] = useState('');
  const [description, setDescription] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      fetchTodo();
    }
  }, [id]);

  const fetchTodo = async () => {
    if (!id) return;
    try {
      const todo = await todoService.getTodo(Number(id));
      setTaskName(todo.task_name);
      setDescription(todo.description);
      setText(todo.text);
    } catch (err) {
      setError('Failed to load todo');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (id) {
        await todoService.updateTodo(Number(id), {
          task_name,
          description,
          text,
        } as Partial<Todo>);
      } else {
        await todoService.createTodo({
          task_name,
          description,
          text,
        } as Partial<Todo>);
      }
      navigate('/todos');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save todo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="todo-form">
        <h2>{id ? 'Edit Todo' : 'Add New Todo'}</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div>
            <label>Task Name</label>
            <input
              type="text"
              value={task_name}
              onChange={(e) => setTaskName(e.target.value)}
              required
              placeholder="Enter task name"
            />
          </div>
          <div>
            <label>Description</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Short description"
            />
          </div>
          <div>
            <label>Details</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter detailed notes..."
              rows={5}
            />
          </div>
          <div className="form-actions">
            <button type="button" onClick={() => navigate('/todos')} className="btn-secondary">
              ← Back to Todos
            </button>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Saving...' : 'Save Todo'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

