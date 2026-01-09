import { useNavigate } from 'react-router-dom';
import { GraduationCap, ArrowRight } from 'lucide-react';
import { motion } from 'motion/react';
import { PageTransition } from './PageTransition';
import { buttonVariants } from '../constants/MotionConstants';

export function HomePage() {
  const navigate = useNavigate();

  return (
    <PageTransition className="min-h-screen bg-white">
      {/* Top Navigation Bar */}
      <nav className="border-b border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-semibold text-gray-900">EduPulse AI</span>
          </div>
          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/login/teacher')}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              Login
            </motion.button>
            <motion.button
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
              onClick={() => navigate('/login/teacher')}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
            >
              Get Started
            </motion.button>
          </div>
        </div>
      </nav>

      {/* Main Content - Centered Role Selector */}
      <div className="flex items-center justify-center" style={{ minHeight: 'calc(100vh - 80px)' }}>
        <div className="text-center max-w-3xl px-6">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl font-semibold text-gray-900 mb-4"
          >
            AI-powered classroom workflows for modern teachers.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-gray-600 mb-16"
          >
            Save hours on grading, analysis, and feedback — while gaining clarity across classrooms.
          </motion.p>

          {/* Role Selector Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <motion.button
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
              onClick={() => navigate('/login/teacher')}
              className="group bg-white border-2 border-gray-200 rounded-xl p-8 hover:border-blue-500 hover:shadow-lg transition-all"
            >
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-500 transition-colors">
                <GraduationCap className="w-8 h-8 text-blue-600 group-hover:text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Continue as Teacher</h3>
              <p className="text-gray-500 mt-2 text-sm">Automate grading & lesson planning</p>
              <div className="flex items-center justify-center text-blue-600 group-hover:gap-2 transition-all mt-4">
                <span>Get started</span>
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </motion.button>

            <motion.button
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
              onClick={() => navigate('/login/student')}
              className="group bg-white border-2 border-gray-200 rounded-xl p-8 hover:border-emerald-500 hover:shadow-lg transition-all"
            >
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-emerald-500 transition-colors">
                <div className="text-2xl">🚀</div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Continue as Student</h3>
              <p className="text-gray-500 mt-2 text-sm">Get instant feedback & support</p>
              <div className="flex items-center justify-center text-emerald-600 group-hover:gap-2 transition-all mt-4">
                <span>Get started</span>
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </motion.button>

            <motion.button
              variants={buttonVariants}
              whileHover="hover"
              whileTap="tap"
              onClick={() => navigate('/login/parent')}
              className="group bg-white border-2 border-gray-200 rounded-xl p-8 hover:border-purple-500 hover:shadow-lg transition-all"
            >
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-purple-500 transition-colors">
                <div className="text-2xl">👨‍👩‍👧</div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Continue as Parent</h3>
              <p className="text-gray-500 mt-2 text-sm">View real-time progress updates</p>
              <div className="flex items-center justify-center text-purple-600 group-hover:gap-2 transition-all mt-4">
                <span>Get started</span>
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </motion.button>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
