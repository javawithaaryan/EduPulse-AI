
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

// --- AI Service Integrations ---

export async function analyzeImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${BASE_URL}/api/vision/analyze`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) throw new Error(`Vision API Failed: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error("Vision Error:", error);
        throw error;
    }
}

export async function askAI(message, history = []) {
    try {
        const response = await fetch(`${BASE_URL}/api/openai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history }),
        });
        if (!response.ok) throw new Error(`OpenAI API Failed: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error("Chat Error:", error);
        throw error;
    }
}

export async function checkMLHealth() {
    try {
        const response = await fetch(`${BASE_URL}/api/ml/health`);
        return {
            ok: response.ok,
            data: response.ok ? await response.json() : null,
            status: response.status
        };
    } catch (error) {
        console.error("ML Health Error:", error);
        return { ok: false, error: error.message };
    }
}

export async function predictStudentRisk(studentData) {
    try {
        const response = await fetch(`${BASE_URL}/api/ml/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(studentData),
        });
        if (!response.ok) throw new Error(`ML Predict Failed: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error("ML Prediction Error:", error);
        throw error;
    }
}
