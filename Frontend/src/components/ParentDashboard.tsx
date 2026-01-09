import { GraduationCap, LogOut, TrendingUp, AlertCircle, BookOpen, Lightbulb, Calendar, CheckCircle2 } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { motion } from 'motion/react';
import { useState, useEffect } from 'react';
import { predictStudentRisk } from '../api';

export function ParentDashboard() {
  const { user, logout } = useApp();
  const userName = user?.name || 'Parent';

  const students = [
    { id: 'BHOOMI-001', name: 'Bhoomi Rathore', grade: 'Grade 10', section: 'A' },
    { id: 'SNEHA-001', name: 'Sneha Patak', grade: 'Grade 8', section: 'B' }
  ];

  const [currentStudent, setCurrentStudent] = useState(students[0]);
  const [riskData, setRiskData] = useState<any>(null);

  useEffect(() => {
    // Fetch real ML risk prediction for selected student
    const fetchRisk = async () => {
      try {
        // Mock data inputs slightly different for each to show variety
        const mockScores = currentStudent.id === 'BHOOMI-001' ? [8, 9, 9, 8.5] : [7, 6, 7.5, 7];
        const mockAttendance = currentStudent.id === 'BHOOMI-001' ? 96 : 88;

        const data = await predictStudentRisk({
          student_id: currentStudent.id,
          recent_scores: mockScores,
          attendance_rate: mockAttendance
        });
        setRiskData(data);
      } catch (e) {
        console.error("Failed to fetch risk", e);
      }
    };
    fetchRisk();
  }, [currentStudent]);


  // Calm, slower animations for parent view
  const containerVariants: any = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15, // Slower stagger
        delayChildren: 0.1
      }
    }
  };

  const itemVariants: any = {
    hidden: { opacity: 0, y: 15 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6, // Slower duration
        ease: "easeOut"
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GraduationCap className="w-8 h-8 text-green-600" />
            <div>
              <div className="text-xl font-semibold text-gray-900">EduPulse AI</div>
              <div className="text-sm text-gray-600">Parent Dashboard</div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right flex items-center gap-3">
              <div>
                <div className="text-sm font-medium text-gray-900">{userName}</div>
                <select
                  className="text-xs text-gray-600 bg-transparent border-none focus:ring-0 cursor-pointer"
                  value={currentStudent.id}
                  onChange={(e) => setCurrentStudent(students.find(s => s.id === e.target.value) || students[0])}
                >
                  {students.map(s => (
                    <option key={s.id} value={s.id}>Viewing: {s.name}</option>
                  ))}
                </select>
              </div>
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
        className="max-w-7xl mx-auto px-6 py-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Child's Overview Banner */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8 group hover:shadow-md transition-shadow"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
              👧
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">{currentStudent.name}'s Learning Journey</h1>
              <p className="text-gray-600">{currentStudent.grade} • Section {currentStudent.section} • St. Xavier's High School</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <div className="text-sm text-green-900 mb-1">Overall Attendance</div>
              <div className="text-2xl font-bold text-green-700">96%</div>
              <div className="w-full bg-green-200 rounded-full h-1.5 mt-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '96%' }}
                  transition={{ duration: 1.5, ease: "easeOut" }}
                  className="bg-green-600 h-1.5 rounded-full"
                />
              </div>
            </div>
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <div className="text-sm text-blue-900 mb-1">Assignments Submitted</div>
              <div className="text-2xl font-bold text-blue-700">24/26</div>
              <div className="w-full bg-blue-200 rounded-full h-1.5 mt-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '92%' }}
                  transition={{ duration: 1.5, ease: "easeOut", delay: 0.2 }}
                  className="bg-blue-600 h-1.5 rounded-full"
                />
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <div className="text-sm text-purple-900 mb-1">Average Grade</div>
              <div className="text-2xl font-bold text-purple-700">A- (88%)</div>
              <div className="w-full bg-purple-200 rounded-full h-1.5 mt-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '88%' }}
                  transition={{ duration: 1.5, ease: "easeOut", delay: 0.4 }}
                  className="bg-purple-600 h-1.5 rounded-full"
                />
              </div>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            {/* Recent Highlights */}
            <motion.div variants={itemVariants} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-blue-600" />
                Recent Highlights
              </h2>
              <div className="space-y-4">
                <div className="flex gap-4 p-4 bg-blue-50 border border-blue-100 rounded-lg">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    🏆
                  </div>
                  <div>
                    <h3 className="font-medium text-blue-900">Excellent Performance in History</h3>
                    <p className="text-sm text-blue-800 mt-1">
                      {currentStudent.name.split(' ')[0]} scored 95% in "Ancient Civilizations". The AI noted her strong essay writing skills.
                    </p>
                  </div>
                </div>
                <div className="flex gap-4 p-4 bg-green-50 border border-green-100 rounded-lg">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                    ✅
                  </div>
                  <div>
                    <h3 className="font-medium text-green-900">Math Homework Completed Early</h3>
                    <p className="text-sm text-green-800 mt-1">
                      Submitted "Algebra Basics" 2 days before the deadline.
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Areas for Focus */}
            <motion.div variants={itemVariants} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-amber-600" />
                Areas for Focus (AI Insights)
              </h2>
              <div className="space-y-4">
                {riskData ? (
                  <div className={`p-4 border rounded-lg ${riskData.risk_level === 'high' ? 'border-red-200 bg-red-50' :
                    riskData.risk_level === 'medium' ? 'border-amber-200 bg-amber-50' :
                      'border-green-200 bg-green-50'
                    }`}>
                    <h3 className="font-medium text-gray-900 mb-2 capitalize">
                      Overall Risk Level: <span className={
                        riskData.risk_level === 'high' ? 'text-red-700' :
                          riskData.risk_level === 'medium' ? 'text-amber-700' :
                            'text-green-700'
                      }>{riskData.risk_level}</span>
                    </h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Startling Trend: <strong>{riskData.trend}</strong>.
                      Confidence: {(riskData.confidence * 100).toFixed(0)}%.
                    </p>
                    <div className="text-sm text-gray-800">
                      <strong>AI Recommendation:</strong> {
                        riskData.risk_level === 'high' ? "Immediate intervention required. Schedule meeting with teacher." :
                          riskData.risk_level === 'medium' ? "Monitor upcoming quiz grades closely. Encourage extra practice." :
                            "Performance is stable. Keep up the good encouragement!"
                      }
                    </div>
                  </div>
                ) : (
                  <div className="p-4 border border-gray-200 rounded-lg animate-pulse bg-gray-50">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  </div>
                )}
              </div>
            </motion.div>

          </div>

          <div className="space-y-6">
            {/* Upcoming */}
            <motion.div variants={itemVariants} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-purple-600" />
                Upcoming Events
              </h2>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="text-center w-12 bg-purple-50 rounded p-1">
                    <div className="text-xs text-purple-600 font-bold uppercase">Oct</div>
                    <div className="text-lg font-bold text-purple-900">12</div>
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Parent-Teacher Meeting</div>
                    <div className="text-xs text-gray-500">10:00 AM - School Hall</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-center w-12 bg-blue-50 rounded p-1">
                    <div className="text-xs text-blue-600 font-bold uppercase">Oct</div>
                    <div className="text-lg font-bold text-blue-900">15</div>
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Science Fair Project Due</div>
                    <div className="text-xs text-gray-500">Submission Online</div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Quick Tips */}
            <motion.div variants={itemVariants} className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
              <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-300" />
                Weekly Parenting Tip
              </h2>
              <p className="text-indigo-100 text-sm mb-4">
                "Encourage 'growth mindset' by praising effort rather than intelligence. Say 'Great work figuring that out' instead of 'You're so smart'."
              </p>
              <div className="text-xs text-indigo-200 italic">- Curated by EduPulse AI</div>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
