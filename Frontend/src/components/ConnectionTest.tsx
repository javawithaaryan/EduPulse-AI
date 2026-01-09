import React, { useEffect, useState } from 'react';
import { pingBackend, uploadFile } from '../api';

const ConnectionTest: React.FC = () => {
    const [status, setStatus] = useState<string>('Checking connection...');
    const [uploadMsg, setUploadMsg] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        pingBackend()
            .then((data) => setStatus(data.status))
            .catch(() => setStatus('Backend disconnected ❌'));
    }, []);

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        setLoading(true);
        setUploadMsg('');
        try {
            const result = await uploadFile(file);
            setUploadMsg(`Success: ${result.message} (${result.filename})`);
        } catch (error) {
            setUploadMsg('Error uploading file ❌');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-4 border rounded shadow-md bg-white m-4 max-w-md">
            <h2 className="text-xl font-bold mb-4">🔌 Backend Connection Test</h2>

            <div className="mb-4">
                <strong>Status: </strong>
                <span className={status.includes('connected') ? 'text-green-600' : 'text-red-500'}>
                    {status}
                </span>
            </div>

            <div className="border-t pt-4">
                <h3 className="font-semibold mb-2">Test File Upload</h3>
                <input
                    type="file"
                    onChange={handleFileChange}
                    disabled={loading}
                    className="block w-full text-sm text-slate-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-violet-50 file:text-violet-700
            hover:file:bg-violet-100"
                />
                {loading && <p className="text-blue-500 mt-2">Uploading...</p>}
                {uploadMsg && <p className="mt-2 text-sm font-mono">{uploadMsg}</p>}
            </div>
        </div>
    );
};

export default ConnectionTest;
