import axios, {AxiosError} from 'axios';

export function apiUrl(endpoint: string): string {
    return `http://localhost:8080/${endpoint}`;
}

export async function sendRequest(
    method: string,
    url: string,
    query = {},
    data: object | null = null,
    headers = {},
) {
    const params = new URLSearchParams(query);
    try {
        const response = await axios({
            method: method,
            url: `${url}?${params.toString()}`,
            data: data,
            headers: headers,
        })
        return {
            success: response.status >= 200 && response.status < 300,
            data: response.data,
            status: response.status
        };
    } catch (error: unknown) {
        return {
            success: false,
            status: (error as AxiosError).response?.status,
            data: (error as AxiosError).response?.data
        };
    }
}


export async function sendAuthRequest(
    method: string,
    url: string,
    authToken: string | null,
    data: object | null = null,
    query = {},
) {
    return sendRequest(
        method, url, query, data, `Authorization: Bearer ${authToken}`
    );
}
