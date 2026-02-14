import axios from 'axios';

const API = axios.create({
  baseURL: 'https://money-stories-final.onrender.com', // Matches your Python FastAPI port
});

export const uploadFile = (formData) => API.post('/api/upload', formData);

export default API;
