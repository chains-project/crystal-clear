// for fetching data from the API

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

export default API_BASE_URL;


export const apiFetch = async <T>(
    path: string,
    alert: (msg: string) => void,
    options: RequestInit = {}
): Promise<T> => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);
    console.log(`Calling API with path: ${path}`);
    console.log(`API_BASE_URL: ${API_BASE_URL}`);

    try {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            headers: { 'Content-Type': 'application/json' },
            signal: controller.signal,
            ...options,
        });

        if (!response.ok) {
            console.log("response", response);
            console.log("response.status", response.status);
            const errorText = await response.text();
            alert(errorText || `Request failed with status ${response.status}`);
            throw new Error(errorText || `Request failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') {
            alert('Request timed out.');
        } else if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            alert('Cannot connect to the backend. Is it running at http://localhost:8000?');
        } else if (error instanceof Error) {
            alert(error.message);
        } else {
            alert('Unknown error occurred.');
        }
        throw error;
    } finally {
        clearTimeout(timeoutId);
    }
};
