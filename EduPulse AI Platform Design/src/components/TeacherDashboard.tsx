import { useState, useEffect } from 'react';
import { GraduationCap, LogOut, Clock, Upload, BarChart3, Users, FileText, QrCode, CheckCircle2, AlertCircle, TrendingDown, Lightbulb, FileCheck, Zap } from 'lucide-react';
import { motion, AnimatePresence, useMotionValue, useTransform, animate } from 'motion/react';
import { AIGradingWorkflow } from './AIGradingWorkflow';
import { useApp } from '../context/AppContext';

export function TeacherDashboard() {
  const { user, logout } = useApp();
  const userName = user?.name || 'Teacher';
  const [showAIGrading, setShowAIGrading] = useState(false);
  const [timesSaved, setTimesSaved] = useState(0);
  const [showToast, setShowToast] = useState(false);

  // Animate time counter
  useEffect(() => {
    const timer = setInterval(() => {
      setTimesSaved(prev => {
        if (prev >= 2.4) return 2.4;
        return Math.min(prev + 0.1, 2.4);
      });
    }, 50);
    return () => clearInterval(timer);
  }, []);

  const handleActionClick = (action: string) => {
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2000);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.08
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Toast Notification */}
      <AnimatePresence>
        {showToast && (
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2"
          >
            <CheckCircle2 className="w-5 h-5" />
            <span>Action completed successfully!</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GraduationCap className="w-8 h-8 text-blue-600" />
            <div>
              <div className="text-xl font-semibold text-gray-900">EduPulse AI</div>
              <div className="text-sm text-gray-600">Teacher Dashboard</div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm font-medium text-gray-900">{userName}</div>
              <div className="text-xs text-gray-600">Grade 7 - Mathematics</div>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={logout}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
            >
              <LogOut className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </nav>

      <motion.div
        className="max-w-7xl mx-auto px-6 py-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Effectiveness Banner with Animation */}
        <motion.div
          variants={itemVariants}
          className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-600 bg-[length:200%_100%] rounded-xl p-6 mb-8 text-white relative overflow-hidden shadow-lg"
        >
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
          <div className="relative z-10 flex items-center gap-4">
            <motion.div
              animate={{
                scale: [1, 1.1, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <Zap className="w-10 h-10 text-yellow-300" />
            </motion.div>
            <div className="flex-1">
              <div className="flex items-baseline gap-2 mb-1">
                <span className="text-2xl font-semibold">EduPulse saved you ~2.4 hours today</span>
              </div>
              <div className="text-blue-100">
                Grading, analysis, and feedback — handled by AI.
              </div>
            </div>
            <div className="text-right">
              <motion.div
                className="text-4xl font-bold"
                key={timesSaved}
              >
                {timesSaved.toFixed(1)}h
              </motion.div>
              <div className="text-blue-200 text-sm">saved today</div>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content Area - AI Grading */}
          <div className="lg:col-span-2">
            {!showAIGrading ? (
              <motion.div
                variants={itemVariants}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 hover:shadow-lg transition-all"
              >
                <div className="text-center max-w-xl mx-auto">
                  <motion.div
                    whileHover={{ scale: 1.05, rotate: 5 }}
                    className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6"
                  >
                    <FileCheck className="w-10 h-10 text-blue-600" />
                  </motion.div>
                  <h2 className="text-3xl font-semibold text-gray-900 mb-3">
                    AI Checking & Grading
                  </h2>
                  <p className="text-gray-600 mb-8">
                    Upload answer sheets or marks. No manual grading required.
                  </p>
                  <motion.button
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowAIGrading(true)}
                    className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-medium shadow-lg shadow-blue-600/30 relative overflow-hidden group"
                  >
                    <motion.div
                      className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
                      transition={{ duration: 0.3 }}
                    />
                    <Upload className="w-6 h-6" />
                    Start AI Grading
                  </motion.button>
                  <p className="text-sm text-gray-500 mt-4">
                    Supports PDF, Images, CSV • Instant analysis • Auto-generated feedback
                  </p>
                </div>

                {/* Recent Activity Preview */}
                <div className="mt-12 pt-8 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Assessments</h3>
                  <div className="space-y-3">
                    <motion.div
                      whileHover={{ x: 4, scale: 1.01 }}
                      className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                        <div>
                          <div className="font-medium text-gray-900">Algebra Quiz - Chapter 4</div>
                          <div className="text-sm text-gray-600">32 students • Graded 2 hours ago</div>
                        </div>
                      </div>
                      <div className="text-sm font-medium text-green-700">Complete</div>
                    </motion.div>
                    <motion.div
                      whileHover={{ x: 4, scale: 1.01 }}
                      className="flex items-center justify-between p-4 bg-gray-50 border border-gray-200 rounded-lg cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        <CheckCircle2 className="w-5 h-5 text-gray-400" />
                        <div>
                          <div className="font-medium text-gray-900">Geometry Test - Unit 2</div>
                          <div className="text-sm text-gray-600">28 students • Graded yesterday</div>
                        </div>
                      </div>
                      <div className="text-sm font-medium text-gray-600">Complete</div>
                    </motion.div>
                  </div>
                </div>
              </motion.div>
            ) : (
              <AIGradingWorkflow onBack={() => setShowAIGrading(false)} />
            )}
          </div>

          {/* Sidebar - Additional Tools */}
          <div className="lg:col-span-1">
            <motion.div
              variants={itemVariants}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-1">Additional Classroom Tools</h3>
              <p className="text-sm text-gray-600 mb-6">Quick access to other features</p>

              <div className="space-y-2">
                <motion.button
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 text-left transition-all border border-gray-200 group relative overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-blue-50 opacity-0 group-hover:opacity-100"
                    transition={{ duration: 0.2 }}
                  />
                  <BarChart3 className="w-5 h-5 text-gray-600 relative z-10" />
                  <span className="text-gray-900 relative z-10">Class Overview</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 text-left transition-all border border-gray-200 group relative overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-blue-50 opacity-0 group-hover:opacity-100"
                    transition={{ duration: 0.2 }}
                  />
                  <Users className="w-5 h-5 text-gray-600 relative z-10" />
                  <span className="text-gray-900 relative z-10">Attendance Marking</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 text-left transition-all border border-gray-200 group relative overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-blue-50 opacity-0 group-hover:opacity-100"
                    transition={{ duration: 0.2 }}
                  />
                  <FileText className="w-5 h-5 text-gray-600 relative z-10" />
                  <span className="text-gray-900 relative z-10">Assignment Creation</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 text-left transition-all border border-gray-200 group relative overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-blue-50 opacity-0 group-hover:opacity-100"
                    transition={{ duration: 0.2 }}
                  />
                  <QrCode className="w-5 h-5 text-gray-600 relative z-10" />
                  <span className="text-gray-900 relative z-10">Classroom QR Generation</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setShowAIGrading(true)}
                  className="w-full flex items-center gap-3 p-3 rounded-lg bg-blue-50 text-left transition-all border-2 border-blue-600 group relative overflow-hidden"
                >
                  <motion.div
                    className="absolute inset-0 bg-blue-100 opacity-0 group-hover:opacity-100"
                    transition={{ duration: 0.2 }}
                  />
                  <FileCheck className="w-5 h-5 text-blue-600 relative z-10" />
                  <span className="text-blue-900 font-medium relative z-10">Checking & Grading</span>
                </motion.button>
              </div>

              {/* Ethical AI Note */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg"
              >
                <div className="flex gap-2">
                  <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div className="text-sm">
                    <div className="font-medium text-amber-900 mb-1">AI Transparency</div>
                    <ul className="text-amber-800 space-y-1 text-xs">
                      <li>• AI suggestions are explainable</li>
                      <li>• Teacher makes final decisions</li>
                      <li>• AI assists, never replaces</li>
                    </ul>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}