import api from './api';

export const authService = {
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    if (response.data.access_token) {
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    if (response.data.access_token) {
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
};

export const mediaService = {
  async upload(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  async list() {
    const response = await api.get('/media/');
    return response.data;
  },

  async get(id) {
    const response = await api.get(`/media/${id}`);
    return response.data;
  },

  async delete(id) {
    const response = await api.delete(`/media/${id}`);
    return response.data;
  }
};

export const platformService = {
  async list() {
    const response = await api.get('/platforms/');
    return response.data;
  },

  async connect(platformData) {
    const response = await api.post('/platforms/connect', platformData);
    return response.data;
  },

  async disconnect(id) {
    const response = await api.delete(`/platforms/${id}`);
    return response.data;
  },

  async enableMonetization(id) {
    const response = await api.post(`/platforms/${id}/monetization`);
    return response.data;
  }
};

export const postService = {
  async create(postData) {
    const response = await api.post('/posts/', postData);
    return response.data;
  },

  async list() {
    const response = await api.get('/posts/');
    return response.data;
  },

  async get(id) {
    const response = await api.get(`/posts/${id}`);
    return response.data;
  },

  async delete(id) {
    const response = await api.delete(`/posts/${id}`);
    return response.data;
  }
};
