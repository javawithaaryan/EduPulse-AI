
const BASE_URL = '';

export async function pingBackend() {
    try {
        const response = await fetch(`${BASE_URL}/ping`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ping failed:", error);
        throw error;
    }
}

export async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Upload error:", error);
        throw error;
    }
}

export async function analyzeData(payload) {
    try {
        const response = await fetch(`${BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Analysis error:", error);
        throw error;
    }
}
