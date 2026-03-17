import axios from 'axios';
import { toast } from 'react-toastify';
import { API_BASE_URL } from '@/config/api';

const LOGIN_PATH = `${import.meta.env.BASE_URL}admin/login`;

// Use env-configured API URL in production, and localhost URL in dev via .env
const axiosInstance = axios.create({
    baseURL: API_BASE_URL || '',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Important for httpOnly cookies
});

// Request interceptor - add JWT token
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle errors and token refresh
axiosInstance.interceptors.response.use(
    (response) => {
        // Extract data from standardized response format
        if (response.data && response.data.data !== undefined) {
            return { ...response, data: response.data.data, message: response.data.message };
        }
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // If 401 and not already retried, try to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshResponse = await axios.post(
                    `/api/v1/auth/refresh`,
                    {},
                    {
                        baseURL: API_BASE_URL || '',
                        withCredentials: true,
                    }
                );

                if (refreshResponse.data.success) {
                    const newToken = refreshResponse.data.data.access_token;
                    localStorage.setItem('access_token', newToken);
                    originalRequest.headers.Authorization = `Bearer ${newToken}`;
                    return axiosInstance(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed, logout user
                localStorage.removeItem('access_token');
                window.location.href = LOGIN_PATH;
                return Promise.reject(refreshError);
            }
        }

        // Show error toast
        const errorMessage =
            error.response?.data?.message ||
            error.response?.data?.detail ||
            error.message ||
            'An error occurred';
        toast.error(errorMessage);

        return Promise.reject(error);
    }
);

export default axiosInstance;
