import api from './api'

export interface LoginRequest {
    username: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export async function login(data: LoginRequest) {
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);
    const response = await api.post("/auth/login", formData);
    return response.data;
}

export async function get_user_name() {
    const user = await api.get("users/me");
    return user.data.name;
}