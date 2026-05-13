// API Types
export interface User {
  id: number;
  username: string;
  email: string;
  is_admin?: boolean;
  first_name?: string;
  last_name?: string;
  date_joined?: string;
}

export interface Todo {
  id: number;
  task_name: string;
  description: string;
  text: string;
  user: User;
  created_at: string;
}

export interface Profile {
  id: number;
  user: User;
  bio: string;
  profile_pic: string;
  location: string;
}

export interface DashboardImage {
  id: number;
  image: string;
  uploaded_at: string;
}

export interface AuthResponse {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
  message: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  password: string;
  email?: string;
}

export interface ChangePasswordData {
  old_password?: string;
  new_password: string;
}

