import api from './api'

export interface CreateAccountRequest {
    name: string;
    balance: number;
}

export async function createAccount(data: CreateAccountRequest) {
    const response = await api.post("/accounts", data);
    return response.data;
}

export async function listAccounts() {
    const response = await api.get("/accounts");
    return response.data;
}

export async function deleteAccount(id: number) {
    const response = await api.delete(`/accounts/${id}`);
    return response.data;
}