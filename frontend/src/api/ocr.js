// ocr.js
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

// Create axios instance with CORS proxy (temporary)
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false, // Important: set to false if CORS isn't configured
  headers: {
    'Content-Type': 'application/json',
  }
});

// For GET requests to /predictions/
export const getPredictions = async () => {
  try {
    const response = await api.get('/predictions/');
    return response.data;
  } catch (error) {
    console.error('Error fetching predictions:', error);
    throw error;
  }
};

// For POST requests - fix the endpoint URL
export const predictImage = async (imageData) => {
  try {
    // Try both endpoints - your backend might expect a different URL
    const response = await api.post('/predict/', imageData);
    return response.data;
  } catch (error) {
    // If /predict/ fails, try /predictions/
    try {
      const response = await api.post('/predictions/', imageData);
      return response.data;
    } catch (secondError) {
      console.error('Error making prediction:', secondError);
      throw secondError;
    }
  }
};