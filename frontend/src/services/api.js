import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API service methods
export const apiService = {
  // Claims endpoints
  getRecentClaims: async (limit = 10) => {
    const response = await apiClient.get(`/claims/recent?limit=${limit}`);
    return response.data;
  },

  // Auth endpoints
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  // Admin endpoints
  getAdminStats: async () => {
    const response = await apiClient.get('/admin/stats');
    return response.data;
  },

  // Prediction endpoints
  predictFraud: async (claimData) => {
    const response = await apiClient.post('/predict', claimData);
    return response.data;
  },

  // Link Analysis endpoints
  getSharedAttributes: async () => {
    const response = await apiClient.get('/link-analysis/shared-attributes');
    return response.data;
  },

  escalateCluster: async (clusterId) => {
    const response = await apiClient.post(`/link-analysis/escalate/${clusterId}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/');
    return response.data;
  },
};

export default apiService;
