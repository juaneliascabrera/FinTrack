import api from './api'

export interface CreateAccountRequest {
    name: string;
    balance: number;
}

export async function createAccount(data: CreateAccountRequest) {
    const response = await api.post("/accounts", data);
    return response.data;
}