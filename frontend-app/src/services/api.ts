import axios, { AxiosInstance } from 'axios';
import {
  User,
  Todo,
  Profile,
  LoginCredentials,
  RegisterCredentials,
  ChangePasswordData,
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

// Get CSRF token from cookies
function getCsrfToken(): string {
  const name = 'csrftoken';
  let cookieValue = '';

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }

  return cookieValue;
}

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fetch CSRF token
export const fetchCsrfToken = async (): Promise<void> => {
  try {
    await axios.get(`${API_BASE_URL}/auth/csrf_token/`, {
      withCredentials: true,
    });
  } catch (error) {
    console.error('Failed to fetch CSRF token', error);
  }
};

// Add CSRF token to every request
api.interceptors.request.use(
  (config) => {
    const csrfToken = getCsrfToken();

    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// =========================
// AUTH SERVICES
// =========================

export const authService = {
  register: async (credentials: RegisterCredentials) => {
    const response = await api.post('/auth/register/', credentials);
    return response.data;
  },

  login: async (credentials: LoginCredentials) => {
    // First fetch csrf token
    await fetchCsrfToken();

    const response = await api.post('/auth/login/', credentials);

    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout/');
    return response.data;
  },

  // me: async () => {
  //   const response = await api.get('/auth/me/');
  //   return response.data as User;
  // },

  changePassword: async (data: ChangePasswordData) => {
    const response = await api.post('/auth/change_password/', data);
    return response.data;
  },
};

// =========================
// TODO SERVICES
// =========================

export const todoService = {
  getTodos: async () => {
    const response = await api.get('/todos/');
    return response.data;
  },

  createTodo: async (data: Partial<Todo>) => {
    const response = await api.post('/todos/', data);
    return response.data;
  },

  updateTodo: async (id: number, data: Partial<Todo>) => {
    const response = await api.patch(`/todos/${id}/`, data);
    return response.data;
  },

  deleteTodo: async (id: number) => {
    const response = await api.delete(`/todos/${id}/`);
    return response.data;
  },
};

// =========================
// PROFILE SERVICES
// =========================

export const profileService = {
  getMyProfile: async () => {
    const response = await api.get('/profiles/my_profile/');
    return response.data as Profile;
  },

  updateProfile: async (data: Partial<Profile>) => {
    const response = await api.patch(
      '/profiles/update_profile/',
      data
    );

    return response.data;
  },
};

export default api;