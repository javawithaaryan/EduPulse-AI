import { GraduationCap, LogOut, Target, BookOpen, Lightbulb, TrendingUp, AlertCircle, CheckCircle2, ArrowRight, Upload, FileText, Brain, Sparkles, Loader2 } from 'lucide-react';
import { motion } from 'motion/react';
import { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';

// Mock Streaming Text Component
function StreamingText({ text }: { text: string }) {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text.charAt(index));
      index++;
      if (index >= text.length) clearInterval(interval);
    }, 20); // Typing speed
    return () => clearInterval(interval);
  }, [text]);

  return <span>{displayedText}</span>;
}

function AskAIChat({ userName, itemVariants }: { userName: string, itemVariants: any }) {
  const [messages, setMessages] = useState<{ role: 'user' | 'ai'; text: string }[]>([
    { role: 'ai', text: `Hi ${userName.split(' ')[0]}! I'm here to help with your studies. Stuck on a problem?` }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setIsTyping(true);

    // Simulate AI thinking and then streaming response
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { role: 'ai', text: "That's a great question! Let's break it down. First, recall the quadratic formula..." }]);
    }, 1500);
  };

  return (
    <motion.div variants={itemVariants} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8 hover:shadow-md transition-shadow">
      <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-purple-600" />
        Ask AI Tutor
      </h2>

      <div className="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto mb-4 flex flex-col gap-3">
        {messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-[80%] rounded-lg p-3 text-sm ${msg.role === 'user'
              ? 'bg-blue-600 text-white rounded-br-none'
              : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
              }`}>
              {msg.role === 'ai' && idx === messages.length - 1 && !isTyping ? (
                <StreamingText text={msg.text} />
              ) : (
                msg.text
              )}
            </div>
          </motion.div>
        ))}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-white border border-gray-200 rounded-lg rounded-bl-none p-3 shadow-sm flex gap-1">
              <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 0.6 }} className="w-2 h-2 bg-gray-400 rounded-full" />
              <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }} className="w-2 h-2 bg-gray-400 rounded-full" />
              <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }} className="w-2 h-2 bg-gray-400 rounded-full" />
            </div>
          </motion.div>
        )}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about Math, Science, or History..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all"
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          disabled={isTyping}
          className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
        >
          <ArrowRight className="w-5 h-5" />
        </motion.button>
      </div>
    </motion.div>
  );
}

export function StudentDashboard() {
  const { user, logout } = useApp();
  const userName = user?.name || 'Aryan';
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success'>('idle');
  const [selectedQuiz, setSelectedQuiz] = useState<string | null>(null);

  const handleUpload = () => {
    setUploadStatus('uploading');
    setTimeout(() => setUploadStatus('success'), 1500);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GraduationCap className="w-8 h-8 text-purple-600" />
            <div>
              <div className="text-xl font-semibold text-gray-900">EduPulse AI</div>
              <div className="text-sm text-gray-600">Student Dashboard</div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm font-medium text-gray-900">{userName}</div>
              <div className="text-xs text-gray-600">Grade 7 - Section A</div>
            </div>
            <button
              onClick={logout}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </nav>

      <motion.div
        className="max-w-5xl mx-auto px-6 py-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Motivational Highlight Card */}
        <motion.div
          variants={itemVariants}
          className="bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 bg-[length:200%_100%] rounded-xl p-8 mb-8 text-white relative overflow-hidden shadow-lg"
        >
          {/* ... existing highlight card content ... */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
            animate={{
              x: ['-100%', '100%']
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "linear"
            }}
          />
          <div className="relative z-10">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="inline-block mb-2"
            >
              <Sparkles className="w-8 h-8 text-yellow-300" />
            </motion.div>
            <motion.h1
              className="text-3xl font-semibold mb-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              You're making great progress, {userName.split(' ')[0]}!
            </motion.h1>
            <motion.p
              className="text-purple-100 text-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              Let's keep the momentum going 🚀
            </motion.p>
          </div>
        </motion.div>

        {/* Ask AI Section */}
        <AskAIChat userName={userName} itemVariants={itemVariants} />

        {/* Assignment Upload Section */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-600" />
            Submit Assignment
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Upload Area */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${uploadStatus === 'success'
                ? 'border-green-500 bg-green-50'
                : 'border-gray-300 hover:border-blue-500 hover:bg-blue-50'
                }`}
              onClick={handleUpload}
            >
              {uploadStatus === 'idle' && (
                <>
                  <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                  <p className="text-sm font-medium text-gray-900 mb-1">Upload Assignment</p>
                  <p className="text-xs text-gray-600">PDF, Image, or Document</p>
                </>
              )}
              {uploadStatus === 'uploading' && (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <Loader2 className="w-12 h-12 text-blue-600 mx-auto mb-3" />
                  </motion.div>
                  <p className="text-sm font-medium text-blue-900">Uploading...</p>
                </>
              )}
              {uploadStatus === 'success' && (
                <>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 200 }}
                  >
                    <CheckCircle2 className="w-12 h-12 text-green-600 mx-auto mb-3" />
                  </motion.div>
                  <p className="text-sm font-medium text-green-900">Submitted Successfully!</p>
                  <p className="text-xs text-green-700 mt-1">AI is reviewing your work</p>
                </>
              )}
            </motion.div>

            {/* Recent Submissions */}
            <div className="space-y-2">
              <p className="text-sm font-medium text-gray-700 mb-3">Recent Submissions</p>

              <motion.div
                whileHover={{ x: 4 }}
                className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg"
              >
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600" />
                  <div>
                    <div className="text-sm font-medium text-gray-900">Math Homework #12</div>
                    <div className="text-xs text-gray-600">Reviewed by AI</div>
                  </div>
                </div>
                <span className="text-xs bg-green-600 text-white px-2 py-1 rounded-full">92%</span>
              </motion.div>

              <motion.div
                whileHover={{ x: 4 }}
                className="flex items-center justify-between p-3 bg-blue-50 border border-blue-200 rounded-lg"
              >
                <div className="flex items-center gap-2">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  >
                    <Brain className="w-4 h-4 text-blue-600" />
                  </motion.div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Science Lab Report</div>
                    <div className="text-xs text-gray-600">AI is reviewing...</div>
                  </div>
                </div>
              </motion.div>

              <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg text-center">
                <p className="text-xs text-gray-600">
                  <Brain className="w-3 h-3 inline mr-1" />
                  AI will review your submission and guide you
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Quiz & Practice Section */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-600" />
            Quiz & Practice
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <motion.button
              whileHover={{ scale: 1.03, y: -2 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => setSelectedQuiz('ai-quiz')}
              className="relative overflow-hidden bg-gradient-to-br from-purple-500 to-blue-600 text-white p-6 rounded-xl shadow-lg group"
            >
              <motion.div
                className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
                transition={{ duration: 0.3 }}
              />
              <Brain className="w-8 h-8 mb-3" />
              <div className="text-left">
                <div className="font-semibold text-lg mb-1">Start AI Quiz</div>
                <div className="text-sm text-purple-100">Adaptive questions based on your level</div>
              </div>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.03, y: -2 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => setSelectedQuiz('practice')}
              className="relative overflow-hidden bg-gradient-to-br from-amber-500 to-orange-600 text-white p-6 rounded-xl shadow-lg group"
            >
              <motion.div
                className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
                transition={{ duration: 0.3 }}
              />
              <Target className="w-8 h-8 mb-3" />
              <div className="text-left">
                <div className="font-semibold text-lg mb-1">Practice Weak Topics</div>
                <div className="text-sm text-amber-100">Focus on quadratic equations</div>
              </div>
            </motion.button>
          </div>

          {/* Progress Tracker */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-900">This Week's Practice</span>
              <span className="text-sm font-semibold text-purple-700">7/10 Sessions</span>
            </div>
            <div className="relative w-full bg-purple-200 rounded-full h-3 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: '70%' }}
                transition={{ duration: 1, ease: "easeOut" }}
                className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full relative"
              >
                <motion.div
                  className="absolute inset-0 bg-white opacity-30"
                  animate={{
                    x: ['-100%', '100%']
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                />
              </motion.div>
            </div>
            <p className="text-xs text-gray-600 mt-2">3 more sessions to unlock achievement! 🏆</p>
          </div>
        </motion.div>

        {/* Recent Assessment Feedback */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            Latest Assessment: Algebra Quiz - Chapter 4
          </h2>

          <div className="flex items-center gap-4 mb-6">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-blue-50 border border-blue-200 rounded-lg px-6 py-4"
            >
              <div className="text-sm text-blue-900 mb-1">Your Score</div>
              <motion.div
                className="text-3xl font-semibold text-blue-700"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: 0.3 }}
              >
                72/100
              </motion.div>
            </motion.div>
            <div className="flex-1 bg-blue-50 border border-blue-200 rounded-lg px-6 py-4">
              <div className="text-sm text-blue-900 mb-2">Class Average: 78%</div>
              <div className="w-full bg-blue-200 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '72%' }}
                  transition={{ duration: 1, ease: "easeOut", delay: 0.5 }}
                  className="bg-blue-600 h-2 rounded-full"
                />
              </div>
            </div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="bg-green-50 border border-green-200 rounded-lg p-4"
          >
            <div className="font-medium text-green-900 mb-2">Teacher's Feedback</div>
            <p className="text-sm text-green-800">
              Good effort, {userName.split(' ')[0]}! You showed strong understanding of linear equations. Focus on practicing quadratic equation word problems and trinomial factoring. Try breaking down problems into smaller steps.
            </p>
          </motion.div>
        </motion.div>

        {/* Mistakes Explained */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-600" />
            Understanding Your Mistakes
          </h2>

          <div className="space-y-4">
            <motion.div
              whileHover={{ x: 4 }}
              className="border border-amber-200 bg-amber-50 rounded-lg p-4"
            >
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-amber-200 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-sm font-semibold text-amber-900">Q3</span>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-amber-900 mb-2">Quadratic Equation - Word Problem</div>
                  <div className="text-sm text-amber-800 mb-2">
                    <strong>What you did:</strong> You solved for x correctly but didn't check if the answer made sense in the context (can't have negative time).
                  </div>
                  <div className="text-sm text-amber-700">
                    <strong>How to improve:</strong> Always read the question carefully and verify your answer fits the real-world context. In this case, choose the positive solution since time cannot be negative.
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ x: 4 }}
              className="border border-amber-200 bg-amber-50 rounded-lg p-4"
            >
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-amber-200 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-sm font-semibold text-amber-900">Q7</span>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-amber-900 mb-2">Factoring Trinomials</div>
                  <div className="text-sm text-amber-800 mb-2">
                    <strong>What you did:</strong> Correct approach, but small calculation error when multiplying factors.
                  </div>
                  <div className="text-sm text-amber-700">
                    <strong>How to improve:</strong> After factoring, multiply back to verify. This catches calculation mistakes before submitting.
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Focus Areas */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-red-600" />
            Your Focus Areas
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="border border-red-200 bg-red-50 rounded-lg p-4"
            >
              <div className="font-medium text-red-900 mb-2">Quadratic Equations</div>
              <div className="text-sm text-red-800 mb-3">
                Word problems and applying the quadratic formula
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-red-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '45%' }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="bg-red-600 h-2 rounded-full"
                  />
                </div>
                <span className="text-xs text-red-700 font-medium">45%</span>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.02 }}
              className="border border-orange-200 bg-orange-50 rounded-lg p-4"
            >
              <div className="font-medium text-orange-900 mb-2">Factoring Trinomials</div>
              <div className="text-sm text-orange-800 mb-3">
                Breaking down complex expressions
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-orange-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '60%' }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="bg-orange-600 h-2 rounded-full"
                  />
                </div>
                <span className="text-xs text-orange-700 font-medium">60%</span>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Personalized Learning Path */}
        <motion.div
          variants={itemVariants}
          className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl border border-purple-200 p-6 mb-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-purple-600" />
            Your Personalized Learning Path
          </h2>

          <p className="text-gray-700 mb-4">
            Based on your recent performance, here's what you should focus on next:
          </p>

          <div className="space-y-3">
            <motion.div
              whileHover={{ scale: 1.02, x: 4 }}
              className="bg-white rounded-lg p-4 border border-purple-200 cursor-pointer"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium text-gray-900">Step 1: Review Quadratic Formula</div>
                <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">15 min</span>
              </div>
              <p className="text-sm text-gray-700 mb-3">
                Watch the recommended video and review your notes on the quadratic formula.
              </p>
              <motion.button
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.95 }}
                className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center gap-1"
              >
                Start Learning
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            </motion.div>

            <div className="bg-white rounded-lg p-4 border border-gray-300 opacity-60">
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium text-gray-900">Step 2: Practice Word Problems</div>
                <span className="text-xs bg-gray-100 text-gray-700 px-3 py-1 rounded-full">20 min</span>
              </div>
              <p className="text-sm text-gray-700 mb-3">
                Complete 5 practice problems focused on real-world applications.
              </p>
              <button className="text-sm text-gray-400 font-medium flex items-center gap-1 cursor-not-allowed">
                Unlock after Step 1
              </button>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-300 opacity-60">
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium text-gray-900">Step 3: Factoring Practice</div>
                <span className="text-xs bg-gray-100 text-gray-700 px-3 py-1 rounded-full">20 min</span>
              </div>
              <p className="text-sm text-gray-700 mb-3">
                Interactive exercises on trinomial factoring with instant feedback.
              </p>
              <button className="text-sm text-gray-400 font-medium flex items-center gap-1 cursor-not-allowed">
                Unlock after Step 2
              </button>
            </div>
          </div>
        </motion.div>

        {/* Progress This Month */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-600" />
            Your Progress This Month
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <motion.div
              whileHover={{ scale: 1.05, y: -4 }}
              className="text-center p-4 bg-green-50 border border-green-200 rounded-lg"
            >
              <CheckCircle2 className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <motion.div
                className="text-2xl font-semibold text-green-700"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", delay: 0.2 }}
              >
                12
              </motion.div>
              <div className="text-sm text-green-900">Assignments Completed</div>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05, y: -4 }}
              className="text-center p-4 bg-blue-50 border border-blue-200 rounded-lg"
            >
              <Target className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <motion.div
                className="text-2xl font-semibold text-blue-700"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", delay: 0.3 }}
              >
                8
              </motion.div>
              <div className="text-sm text-blue-900">Skills Improved</div>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05, y: -4 }}
              className="text-center p-4 bg-purple-50 border border-purple-200 rounded-lg"
            >
              <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <motion.div
                className="text-2xl font-semibold text-purple-700"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: "spring", delay: 0.4 }}
              >
                +5%
              </motion.div>
              <div className="text-sm text-purple-900">Average Improvement</div>
            </motion.div>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}