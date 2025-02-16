import axios from 'axios';

// Create an Axios instance with a base URL
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

// Add a request interceptor to attach the token to every request
axiosInstance.interceptors.request.use(
  (config) => {
    // Retrieve the token from localStorage (or any other storage)
    const token = localStorage.getItem('token');
    if (token) {
      // Attach token to the Authorization header
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
