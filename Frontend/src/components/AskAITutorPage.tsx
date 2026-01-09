import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Send, Paperclip, Sparkles, Image as ImageIcon, X, ChevronRight, Loader2, Bot, User } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { OpenAIService, AIChatMessage } from '../services/OpenAIService';

export function AskAITutorPage() {
    const { user } = useApp();
    const [messages, setMessages] = useState<AIChatMessage[]>([
        {
            id: '1',
            role: 'assistant',
            content: `Hi ${user?.name?.split(' ')[0] || 'there'}! I'm your AI Tutor. I can help you understand concepts, review mistakes, or prepare for your next quiz. What's on your mind?`,
            timestamp: new Date()
        }
    ]);
    const [inputObj, setInputObj] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [streamingContent, setStreamingContent] = useState('');
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, streamingContent]);

    const handleSend = async (manualText?: string) => {
        const textToSend = manualText || inputObj;
        if ((!textToSend.trim() && !selectedFile) || isLoading) return;

        setInputObj('');

        // Add User Message
        const userMsg: AIChatMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: textToSend,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMsg]);
        setIsLoading(true);

        // Placeholder for AI Message being loaded
        const aiMsgId = (Date.now() + 1).toString();
        setMessages(prev => [...prev, {
            id: aiMsgId,
            role: 'assistant',
            content: '', // Start empty for typing indicator
            timestamp: new Date()
        }]);

        try {
            const response = await OpenAIService.sendMessage(
                textToSend,
                {
                    name: user?.name,
                    grade: '7', // Default or from user context
                    subject: 'Math',
                    weakTopics: ['Quadratic Equations']
                }
            );

            setMessages(prev => prev.map(msg =>
                msg.id === aiMsgId ? { ...msg, content: response } : msg
            ));
        } catch (e) {
            setMessages(prev => prev.map(msg =>
                msg.id === aiMsgId ? { ...msg, content: "I'm having trouble right now. Let's try again." } : msg
            ));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto h-[calc(100vh-4rem)] flex flex-col">
            {/* Header */}
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                    <Sparkles className="w-6 h-6 text-purple-600" />
                    Ask AI Tutor
                </h1>
                <p className="text-gray-500">
                    Get help with concepts, mistakes, and what to study next.
                </p>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-4 space-y-6">
                {messages.map((msg) => (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        key={msg.id}
                        className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-blue-100 text-blue-600' : 'bg-purple-100 text-purple-600'
                            }`}>
                            {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                        </div>

                        <div className={`max-w-[80%] rounded-2xl p-4 text-sm leading-relaxed ${msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-tr-none'
                            : 'bg-gray-100 text-gray-800 rounded-tl-none'
                            }`}>
                            {msg.content || (
                                <div className="flex gap-1 items-center h-5">
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                                </div>
                            )}
                        </div>
                    </motion.div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Suggested Chips */}
            {!isLoading && messages.length < 3 && (
                <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
                    {['Explain my recent Quiz mistake', 'How do I solve Quadratics?', 'create a study plan'].map((suggestion) => (
                        <button
                            key={suggestion}
                            onClick={() => handleSend(suggestion)}
                            className="whitespace-nowrap px-4 py-2 bg-purple-50 text-purple-700 rounded-full text-sm font-medium hover:bg-purple-100 transition-colors border border-purple-100"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            )}

            {/* Input Area */}
            <div className="bg-white rounded-2xl border border-gray-200 p-2 shadow-sm relative">
                {selectedFile && (
                    <div className="absolute -top-12 left-0 bg-white border border-gray-200 p-2 rounded-lg flex items-center gap-2 shadow-sm">
                        <div className="bg-gray-100 p-1 rounded">
                            <Paperclip className="w-4 h-4 text-gray-600" />
                        </div>
                        <span className="text-sm text-gray-700 max-w-[200px] truncate">{selectedFile.name}</span>
                        <button onClick={() => setSelectedFile(null)} className="text-gray-400 hover:text-red-500">
                            <X className="w-4 h-4" />
                        </button>
                    </div>
                )}

                <div className="flex items-center gap-2">
                    <input
                        type="file"
                        id="file-upload"
                        className="hidden"
                        onChange={(e) => {
                            if (e.target.files?.[0]) setSelectedFile(e.target.files[0]);
                        }}
                    />
                    <button
                        onClick={() => document.getElementById('file-upload')?.click()}
                        className="p-3 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all"
                        title="Upload file or image"
                    >
                        <Paperclip className="w-5 h-5" />
                    </button>

                    <input
                        type="text"
                        value={inputObj}
                        onChange={(e) => setInputObj(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask about a concept, mistake, or topic..."
                        className="flex-1 bg-transparent border-none focus:ring-0 text-gray-900 placeholder-gray-400 text-base"
                        disabled={isLoading}
                    />

                    <button
                        onClick={() => handleSend()}
                        disabled={(!inputObj.trim() && !selectedFile) || isLoading}
                        className={`p-3 rounded-xl transition-all flex items-center justify-center ${(!inputObj.trim() && !selectedFile) || isLoading
                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                            : 'bg-purple-600 text-white hover:bg-purple-700 shadow-md transform hover:scale-105'
                            }`}
                    >
                        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                    </button>
                </div>
            </div>
        </div>
    );
}
