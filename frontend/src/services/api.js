import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000', // Matches your Python FastAPI port
});

export const uploadFile = (formData) => API.post('/api/upload', formData);

export default API;