import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000'
});

// Interceptor for add the token everywhere.
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Interceptor for handling token expiration (401 errors)
api.interceptors.response.use(
    (response) => {
        // If the request succeeds, just return the response
        return response;
    },
    (error) => {
        // If the server returns 401 Unauthorized, the token is likely expired or invalid
        // BUT we should avoid redirecting if the error comes from the login request itself
        if (error.response && error.response.status === 401) {
            const isLoginRequest = error.config.url.includes('/auth/login');
            
            if (!isLoginRequest) {
                console.warn("Session expired or invalid. Redirecting to login...");
                
                // 1. Clear the token
                localStorage.removeItem('token');
                
                // 2. Redirect to login (force reload to clear any sensitive state)
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
