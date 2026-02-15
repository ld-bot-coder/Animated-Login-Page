import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// API Service
const apiService = {
    // Authentication
    login: async (email, password) => {
        const response = await api.post('/auth', { email, password });
        return response.data;
    },

    // Demo Links
    getDemoLinks: async () => {
        const response = await api.get('/demo-links');
        return response.data;
    },

    createDemoLink: async (linkData) => {
        const response = await api.post('/demo-links', linkData);
        return response.data;
    },

    updateDemoLink: async (id, linkData) => {
        const response = await api.put(`/demo-links/${id}`, linkData);
        return response.data;
    },

    deleteDemoLink: async (id) => {
        const response = await api.delete(`/demo-links/${id}`);
        return response.data;
    },

    // Users
    getUsers: async () => {
        const response = await api.get('/users');
        return response.data;
    },

    createUser: async (userData) => {
        const response = await api.post('/users', userData);
        return response.data;
    },

    updateUser: async (id, userData) => {
        const response = await api.put(`/users/${id}`, userData);
        return response.data;
    },

    deleteUser: async (id) => {
        const response = await api.delete(`/users/${id}`);
        return response.data;
    },

    // Categories
    getCategories: async () => {
        const response = await api.get('/categories');
        return response.data;
    },
};

export default apiService;
