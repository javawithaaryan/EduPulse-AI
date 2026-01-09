import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Eye, MessageSquare, Brain, Upload, Send, Activity,
    CheckCircle, AlertTriangle, XCircle, Loader2
} from 'lucide-react';
import { analyzeImage, askAI, checkMLHealth, predictStudentRisk } from '../api';

export function AIPlayground() {
    const [activeTab, setActiveTab] = useState<'vision' | 'chat' | 'ml'>('vision');

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <header className="max-w-4xl mx-auto mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Service Playground</h1>
                <p className="text-gray-600">Test and demo the integrated Azure AI capabilities.</p>
            </header>

            <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="flex border-b border-gray-200">
                    <button
                        onClick={() => setActiveTab('vision')}
                        className={`flex-1 py-4 px-6 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${activeTab === 'vision' ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'
                            }`}
                    >
                        <Eye size={18} /> Azure AI Vision
                    </button>
                    <button
                        onClick={() => setActiveTab('chat')}
                        className={`flex-1 py-4 px-6 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${activeTab === 'chat' ? 'bg-green-50 text-green-600 border-b-2 border-green-600' : 'text-gray-500 hover:text-gray-700'
                            }`}
                    >
                        <MessageSquare size={18} /> OpenAI Chat
                    </button>
                    <button
                        onClick={() => setActiveTab('ml')}
                        className={`flex-1 py-4 px-6 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${activeTab === 'ml' ? 'bg-purple-50 text-purple-600 border-b-2 border-purple-600' : 'text-gray-500 hover:text-gray-700'
                            }`}
                    >
                        <Brain size={18} /> Azure Machine Learning
                    </button>
                </div>

                <div className="p-6">
                    <AnimatePresence mode="wait">
                        {activeTab === 'vision' && <VisionTab key="vision" />}
                        {activeTab === 'chat' && <ChatTab key="chat" />}
                        {activeTab === 'ml' && <MLTab key="ml" />}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}

// --- Sub-Components ---

function VisionTab() {
    const [image, setImage] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setImage(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
            setError(null);
        }
    };

    const handleAnalyze = async () => {
        if (!image) return;
        setLoading(true);
        setError(null);
        try {
            const data = await analyzeImage(image);
            setResult(data);
        } catch (err: any) {
            setError(err.message || "Failed to analyze image");
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
            <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-4">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50 transition-colors relative">
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        />
                        {preview ? (
                            <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded shadow-sm" />
                        ) : (
                            <div className="py-8 text-gray-400">
                                <Upload className="mx-auto mb-2" size={32} />
                                <p>Click or Drag to Upload Image</p>
                            </div>
                        )}
                    </div>
                    <button
                        onClick={handleAnalyze}
                        disabled={!image || loading}
                        className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                    >
                        {loading && <Loader2 className="animate-spin" size={16} />}
                        {loading ? 'Analyzing...' : 'Analyze Image'}
                    </button>
                    {error && (
                        <div className="p-3 bg-red-50 text-red-700 rounded-lg flex items-center gap-2 text-sm">
                            <AlertTriangle size={16} /> {error}
                        </div>
                    )}
                </div>

                <div className="space-y-4">
                    <h3 className="font-semibold text-gray-700">Analysis Results</h3>
                    {result ? (
                        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-sm overflow-auto max-h-[400px]">
                            {/* Caption */}
                            {result.caption && (
                                <div className="mb-4">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Caption</span>
                                    <p className="text-lg font-medium text-gray-900 mt-1">
                                        "{result.caption}"
                                    </p>
                                </div>
                            )}

                            {/* Tags */}
                            {result.tags && result.tags.length > 0 && (
                                <div className="mb-4">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-2">Tags</span>
                                    <div className="flex flex-wrap gap-2">
                                        {result.tags.map((tag: any, idx: number) => (
                                            <span key={idx} className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                                                {tag.name} {(tag.confidence * 100).toFixed(0)}%
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Objects */}
                            {result.objects && result.objects.length > 0 && (
                                <div className="mb-4">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-2">Detected Objects</span>
                                    <ul className="space-y-1">
                                        {result.objects.map((obj: any, idx: number) => (
                                            <li key={idx} className="flex justify-between text-gray-700">
                                                <span>{obj.tag}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Raw JSON Toggle */}
                            <details className="mt-4">
                                <summary className="cursor-pointer text-blue-600 text-xs hover:underline">View Raw JSON</summary>
                                <pre className="mt-2 text-xs text-gray-500 whitespace-pre-wrap">
                                    {JSON.stringify(result, null, 2)}
                                </pre>
                            </details>
                        </div>
                    ) : (
                        <div className="h-full flex items-center justify-center text-gray-400 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                            <p>Results will appear here</p>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
}

function ChatTab() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string }[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setLoading(true);

        try {
            const data = await askAI(userMsg, messages);
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Error: Failed to get response." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="h-[500px] flex flex-col">
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 mb-4">
                {messages.length === 0 && (
                    <div className="text-center text-gray-400 mt-20">
                        <MessageSquare className="mx-auto mb-2 opacity-20" size={48} />
                        <p>Start a conversation with Azure OpenAI</p>
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-lg px-4 py-2 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-none'
                                : 'bg-gray-100 text-gray-800 rounded-bl-none'
                            }`}>
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg px-4 py-3 rounded-bl-none flex gap-1">
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
                        </div>
                    </div>
                )}
            </div>

            <form onSubmit={handleSend} className="relative">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="w-full pl-4 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-shadow"
                />
                <button
                    type="submit"
                    disabled={!input.trim() || loading}
                    className="absolute right-2 top-2 p-1.5 text-blue-600 hover:bg-blue-50 rounded-md disabled:opacity-50 transition-colors"
                >
                    <Send size={20} />
                </button>
            </form>
        </motion.div>
    );
}

function MLTab() {
    const [health, setHealth] = useState<{ status: string, workspace: string } | null>(null);
    const [checking, setChecking] = useState(false);

    // Prediction Form
    const [studentId, setStudentId] = useState('ST-1001');
    const [scores, setScores] = useState('8, 7, 9, 6');
    const [attendance, setAttendance] = useState(90);
    const [prediction, setPrediction] = useState<any>(null);
    const [predicting, setPredicting] = useState(false);

    useEffect(() => {
        checkHealth();
    }, []);

    const checkHealth = async () => {
        setChecking(true);
        const res = await checkMLHealth();
        if (res.ok) setHealth(res.data);
        else setHealth({ status: 'Error', workspace: 'Connection Failed' });
        setChecking(false);
    };

    const handlePredict = async (e: React.FormEvent) => {
        e.preventDefault();
        setPredicting(true);
        setPrediction(null);
        try {
            const scoreArray = scores.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));
            const data = await predictStudentRisk({
                student_id: studentId,
                recent_scores: scoreArray,
                attendance_rate: attendance
            });
            setPrediction(data);
        } catch (err) {
            console.error(err);
        } finally {
            setPredicting(false);
        }
    };

    return (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-8">
            {/* Connection Status Card */}
            <div className={`p-4 rounded-lg border flex items-center justify-between ${health?.status === 'Connected' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                }`}>
                <div className="flex items-center gap-3">
                    <Activity className={health?.status === 'Connected' ? 'text-green-600' : 'text-red-600'} />
                    <div>
                        <h3 className={`font-semibold ${health?.status === 'Connected' ? 'text-green-900' : 'text-red-900'}`}>
                            Azure ML Status: {checking ? 'Checking...' : (health?.status || 'Unknown')}
                        </h3>
                        {health?.workspace && <p className="text-sm opacity-80">Workspace: {health.workspace}</p>}
                    </div>
                </div>
                <button onClick={checkHealth} className="text-sm underline hover:opacity-80">
                    Refresh
                </button>
            </div>

            {/* Prediction Interface */}
            <div className="grid md:grid-cols-2 gap-8">
                <form onSubmit={handlePredict} className="space-y-4">
                    <h3 className="font-semibold text-gray-800 border-b pb-2">Student Risk Predictor</h3>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Student ID</label>
                        <input type="text" value={studentId} onChange={e => setStudentId(e.target.value)} className="w-full p-2 border rounded-md" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Recent Scores (comma separated)</label>
                        <input type="text" value={scores} onChange={e => setScores(e.target.value)} className="w-full p-2 border rounded-md" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Attendance Rate (%)</label>
                        <input type="range" min="0" max="100" value={attendance} onChange={e => setAttendance(parseInt(e.target.value))} className="w-full" />
                        <div className="text-right text-sm text-gray-500">{attendance}%</div>
                    </div>

                    <button disabled={predicting} className="w-full py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50">
                        {predicting ? 'Predicting...' : 'Run Prediction Model'}
                    </button>
                </form>

                <div className="bg-white border rounded-lg p-6 shadow-sm min-h-[200px] flex flex-col items-center justify-center">
                    {prediction ? (
                        <div className="text-center w-full">
                            <div className="mb-4">
                                <span className={`inline-block p-4 rounded-full ${prediction.risk_level === 'high' ? 'bg-red-100 text-red-600' :
                                        prediction.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                                            'bg-green-100 text-green-600'
                                    }`}>
                                    <Brain size={32} />
                                </span>
                            </div>
                            <h4 className="text-xl font-bold text-gray-800 capitalize mb-1">
                                {prediction.risk_level} Risk
                            </h4>
                            <p className="text-gray-500 text-sm mb-4">
                                Confidence: {(prediction.confidence * 100).toFixed(1)}%
                            </p>

                            <div className="grid grid-cols-2 gap-2 text-sm text-left bg-gray-50 p-3 rounded w-full">
                                <span className="text-gray-500">Trend:</span>
                                <span className="font-medium">{prediction.trend}</span>
                                <span className="text-gray-500">Impact:</span>
                                <span className="font-medium">{prediction.attendance_impact}</span>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-400 text-center">
                            Enter student data and run prediction to see AI analysis.
                        </p>
                    )}
                </div>
            </div>
        </motion.div>
    );
}
