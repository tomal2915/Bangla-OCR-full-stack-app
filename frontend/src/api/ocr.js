import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

const api = axios.create({
  baseURL: BASE_URL,
});

// POST /api/predict/ — send image, get back character + confidence
export const predictCharacter = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await api.post('/api/predict/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return response.data;
};

// GET /api/predictions/ — fetch last 20 predictions
export const fetchHistory = async () => {
  const response = await api.get('/api/predictions/');
  return response.data;
};