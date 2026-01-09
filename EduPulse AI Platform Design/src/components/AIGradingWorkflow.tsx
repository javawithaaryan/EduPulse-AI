import { useState, useEffect } from 'react';
import { ArrowLeft, Upload, Loader2, CheckCircle2, AlertTriangle, TrendingDown, Users, Lightbulb, Edit3, Send } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface AIGradingWorkflowProps {
  onBack: () => void;
}

type WorkflowState = 'upload' | 'processing' | 'complete';

export function AIGradingWorkflow({ onBack }: AIGradingWorkflowProps) {
  const [state, setState] = useState<WorkflowState>('upload');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (state === 'processing') {
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            setState('complete');
            return 100;
          }
          return prev + 2;
        });
      }, 50);
      return () => clearInterval(interval);
    }
  }, [state]);

  const handleFileUpload = () => {
    setState('processing');
  };

  const handleUseDemoData = () => {
    setState('processing');
  };

  if (state === 'upload') {
    return (
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
      >
        <motion.button
          whileHover={{ x: -4 }}
          whileTap={{ scale: 0.95 }}
          onClick={onBack}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to dashboard
        </motion.button>

        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Upload Assessment</h2>

        {/* Upload Area */}
        <motion.div 
          whileHover={{ scale: 1.01, borderColor: '#3b82f6' }}
          whileTap={{ scale: 0.99 }}
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-blue-500 transition-all cursor-pointer mb-6 group"
        >
          <motion.div
            whileHover={{ y: -5 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <Upload className="w-16 h-16 text-gray-400 group-hover:text-blue-500 mx-auto mb-4 transition-colors" />
          </motion.div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Drop files here or click to upload
          </h3>
          <p className="text-gray-600 mb-4">
            Supports PDF, JPG, PNG, CSV files
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleFileUpload}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors relative overflow-hidden group"
          >
            <motion.div
              className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
              transition={{ duration: 0.3 }}
            />
            Select Files
          </motion.button>
        </motion.div>

        <div className="relative mb-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-white text-gray-500">Or</span>
          </div>
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleUseDemoData}
          className="w-full border-2 border-blue-600 text-blue-600 py-3 rounded-lg hover:bg-blue-50 transition-colors font-medium"
        >
          Use Demo Assessment Data
        </motion.button>

        {/* What happens next */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg"
        >
          <h4 className="font-medium text-blue-900 mb-2">What happens after upload:</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>✓ AI grades all submissions automatically</li>
            <li>✓ Identifies learning gaps and weak concepts</li>
            <li>✓ Generates personalized feedback for each student</li>
            <li>✓ Creates remedial lesson plan recommendations</li>
          </ul>
        </motion.div>
      </motion.div>
    );
  }

  if (state === 'processing') {
    return (
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
      >
        <div className="text-center max-w-md mx-auto">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <Loader2 className="w-16 h-16 text-blue-600 mx-auto mb-6" />
          </motion.div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">AI Grading in Progress</h2>
          <p className="text-gray-600 mb-6">
            Analyzing answer sheets and generating insights...
          </p>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-3 mb-2 overflow-hidden">
            <motion.div
              className="bg-blue-600 h-3 rounded-full relative"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                animate={{
                  x: ['-100%', '100%']
                }}
                transition={{
                  duration: 1,
                  repeat: Infinity,
                  ease: "linear"
                }}
              />
            </motion.div>
          </div>
          <p className="text-sm text-gray-600">{progress}% complete</p>

          {/* Processing Steps */}
          <div className="mt-8 text-left space-y-3">
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ 
                opacity: progress > 20 ? 1 : 0.4,
                x: 0
              }}
              className={`flex items-center gap-3 ${progress > 20 ? 'text-green-700' : 'text-gray-400'}`}
            >
              <motion.div
                animate={progress > 20 ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                <CheckCircle2 className="w-5 h-5" />
              </motion.div>
              <span className="text-sm">Scanning answer sheets</span>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ 
                opacity: progress > 40 ? 1 : 0.4,
                x: 0
              }}
              transition={{ delay: 0.1 }}
              className={`flex items-center gap-3 ${progress > 40 ? 'text-green-700' : 'text-gray-400'}`}
            >
              <motion.div
                animate={progress > 40 ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                <CheckCircle2 className="w-5 h-5" />
              </motion.div>
              <span className="text-sm">Grading submissions</span>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ 
                opacity: progress > 60 ? 1 : 0.4,
                x: 0
              }}
              transition={{ delay: 0.2 }}
              className={`flex items-center gap-3 ${progress > 60 ? 'text-green-700' : 'text-gray-400'}`}
            >
              <motion.div
                animate={progress > 60 ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                <CheckCircle2 className="w-5 h-5" />
              </motion.div>
              <span className="text-sm">Identifying learning gaps</span>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ 
                opacity: progress > 80 ? 1 : 0.4,
                x: 0
              }}
              transition={{ delay: 0.3 }}
              className={`flex items-center gap-3 ${progress > 80 ? 'text-green-700' : 'text-gray-400'}`}
            >
              <motion.div
                animate={progress > 80 ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                <CheckCircle2 className="w-5 h-5" />
              </motion.div>
              <span className="text-sm">Generating feedback</span>
            </motion.div>
          </div>
        </div>
      </motion.div>
    );
  }

  // Complete state
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
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <motion.button
        whileHover={{ x: -4 }}
        whileTap={{ scale: 0.95 }}
        onClick={onBack}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to dashboard
      </motion.button>

      {/* Success Banner */}
      <motion.div 
        variants={itemVariants}
        className="bg-green-50 border border-green-200 rounded-xl p-6"
      >
        <div className="flex items-center gap-3">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
          >
            <CheckCircle2 className="w-8 h-8 text-green-600" />
          </motion.div>
          <div>
            <h2 className="text-xl font-semibold text-green-900">AI Analysis Complete!</h2>
            <p className="text-green-700">Algebra Quiz - Chapter 4 • 32 students graded</p>
          </div>
        </div>
      </motion.div>

      {/* AI Class Summary */}
      <motion.div 
        variants={itemVariants}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-blue-600" />
          AI Class Summary
        </h3>
        
        <div className="grid grid-cols-3 gap-4 mb-6">
          <motion.div 
            whileHover={{ scale: 1.05, y: -4 }}
            className="bg-green-50 border border-green-200 rounded-lg p-4"
          >
            <motion.div 
              className="text-3xl font-semibold text-green-700"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", delay: 0.2 }}
            >
              78%
            </motion.div>
            <div className="text-sm text-green-900">Average Score</div>
          </motion.div>
          <motion.div 
            whileHover={{ scale: 1.05, y: -4 }}
            className="bg-red-50 border border-red-200 rounded-lg p-4"
          >
            <motion.div 
              className="text-3xl font-semibold text-red-700"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", delay: 0.3 }}
            >
              8
            </motion.div>
            <div className="text-sm text-red-900">Need Attention</div>
          </motion.div>
          <motion.div 
            whileHover={{ scale: 1.05, y: -4 }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-4"
          >
            <motion.div 
              className="text-3xl font-semibold text-blue-700"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", delay: 0.4 }}
            >
              32
            </motion.div>
            <div className="text-sm text-blue-900">Auto-Graded</div>
          </motion.div>
        </div>

        {/* Weak Concepts Identified */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h4 className="font-medium text-red-900 mb-2 flex items-center gap-2">
            <TrendingDown className="w-4 h-4" />
            Weak Concepts Identified
          </h4>
          <div className="space-y-2">
            {['Quadratic Equations (Standard Form)', 'Factoring Trinomials', 'Word Problems (Application)'].map((concept, index) => (
              <motion.div 
                key={concept}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                whileHover={{ x: 4 }}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-red-800">{concept}</span>
                <span className="text-red-700 font-medium">{18 - index * 4} students struggled</span>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* AI Suggested Remedial Plan */}
      <motion.div 
        variants={itemVariants}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-600" />
          AI Suggested Remedial Plan
        </h3>

        <div className="space-y-4">
          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="border border-gray-200 rounded-lg p-4"
          >
            <div className="font-medium text-gray-900 mb-2">📚 What to Revise</div>
            <ul className="text-sm text-gray-700 space-y-1 ml-4">
              <li>• Review quadratic equation solving methods (factoring, completing square, formula)</li>
              <li>• Practice trinomial factoring with step-by-step examples</li>
              <li>• Use real-world word problems to connect concepts</li>
            </ul>
          </motion.div>

          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="border border-gray-200 rounded-lg p-4"
          >
            <div className="font-medium text-gray-900 mb-2 flex items-center gap-2">
              <Users className="w-4 h-4" />
              Students to Group
            </div>
            <p className="text-sm text-gray-700 mb-2">Group A (Quadratic Equations): 18 students</p>
            <div className="flex flex-wrap gap-2">
              {['Alex Chen', 'Emma Rodriguez', 'Marcus Williams', 'Sofia Martinez'].map((name) => (
                <motion.span
                  key={name}
                  whileHover={{ scale: 1.1 }}
                  className="text-xs bg-gray-100 px-2 py-1 rounded cursor-pointer"
                >
                  {name}
                </motion.span>
              ))}
              <span className="text-xs bg-gray-100 px-2 py-1 rounded">+14 more</span>
            </div>
          </motion.div>

          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="border border-gray-200 rounded-lg p-4"
          >
            <div className="font-medium text-gray-900 mb-2">⏱️ Recommended Time</div>
            <p className="text-sm text-gray-700">2 class periods (80 minutes) + 1 homework assignment</p>
          </motion.div>
        </div>

        <motion.button 
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="mt-4 w-full bg-amber-600 text-white py-3 rounded-lg hover:bg-amber-700 transition-colors font-medium relative overflow-hidden group"
        >
          <motion.div
            className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
            transition={{ duration: 0.3 }}
          />
          Apply Remedial Plan to Calendar
        </motion.button>
      </motion.div>

      {/* AI-Drafted Student Feedback */}
      <motion.div 
        variants={itemVariants}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
          <Edit3 className="w-5 h-5 text-purple-600" />
          AI-Drafted Student Feedback
        </h3>
        <p className="text-sm text-gray-600 mb-4">Pre-written feedback for each student • Editable by teacher</p>

        <div className="space-y-3">
          {[
            { name: 'Alex Chen', score: '72/100', feedback: 'Good effort, Alex! You showed strong understanding of linear equations. Focus on practicing quadratic equation word problems and trinomial factoring. Try breaking down problems into smaller steps.' },
            { name: 'Emma Rodriguez', score: '68/100', feedback: 'Emma, you\'re making progress! Your algebraic manipulation skills are improving. Spend extra time on completing the square method and practice more application problems to build confidence.' },
            { name: 'Marcus Williams', score: '89/100', feedback: 'Excellent work, Marcus! You demonstrated mastery of most concepts. To reach the next level, focus on optimizing your problem-solving approach for word problems and check your work carefully.' }
          ].map((student, index) => (
            <motion.div 
              key={student.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.01, x: 4 }}
              className="border border-gray-200 rounded-lg p-4 bg-gray-50"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium text-gray-900">{student.name}</div>
                <div className="text-sm text-gray-600">Score: {student.score}</div>
              </div>
              <p className="text-sm text-gray-700 mb-3">
                {student.feedback}
              </p>
              <div className="flex gap-2">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1"
                >
                  <Edit3 className="w-3 h-3" />
                  Edit
                </motion.button>
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="text-sm text-green-600 hover:text-green-700 flex items-center gap-1"
                >
                  <Send className="w-3 h-3" />
                  Send
                </motion.button>
              </div>
            </motion.div>
          ))}

          <button className="w-full text-center text-sm text-gray-600 hover:text-gray-900 py-2">
            View all 32 student feedbacks →
          </button>
        </div>

        <div className="mt-4 flex gap-3">
          <motion.button 
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium relative overflow-hidden group"
          >
            <motion.div
              className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
              transition={{ duration: 0.3 }}
            />
            Send All Feedback
          </motion.button>
          <motion.button 
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 transition-colors font-medium"
          >
            Review & Edit
          </motion.button>
        </div>
      </motion.div>
    </motion.div>
  );
}