import { useState } from 'react';
import { BookOpen, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';

export function StudentSignIn() {
  const navigate = useNavigate();
  const { login } = useApp();
  const [studentId, setStudentId] = useState('');
  const [email, setEmail] = useState('');

  const handleDemoLogin = () => {
    login('student', 'Alex Chen');
    navigate('/student/dashboard');
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    login('student', 'Student');
    navigate('/student/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-white flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to home
        </button>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex items-center justify-center mb-6">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
              <BookOpen className="w-8 h-8 text-purple-600" />
            </div>
          </div>

          <h2 className="text-3xl font-semibold text-center text-gray-900 mb-2">Student Sign In</h2>
          <p className="text-center text-gray-600 mb-8">Access your learning dashboard</p>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label htmlFor="student-id" className="block text-sm font-medium text-gray-700 mb-2">
                Student ID
              </label>
              <input
                type="text"
                id="student-id"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                placeholder="STU2024001"
              />
            </div>

            <div>
              <label htmlFor="student-email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="student-email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                placeholder="student@school.edu"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium"
            >
              Sign In
            </button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-gray-500">Or try a demo</span>
            </div>
          </div>

          <button
            onClick={handleDemoLogin}
            className="w-full border-2 border-purple-600 text-purple-600 py-3 rounded-lg hover:bg-purple-50 transition-colors font-medium"
          >
            Demo Student Login
          </button>
        </div>
      </div>
    </div>
  );
}
