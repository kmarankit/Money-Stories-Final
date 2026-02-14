import axios from 'axios';

const API = axios.create({
  baseURL: 'VITE_API_BASE_URL', // Matches your Python FastAPI port
});

export const uploadFile = (formData) => API.post('/api/upload', formData);

export default API;