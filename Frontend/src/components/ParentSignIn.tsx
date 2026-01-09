import { useState } from 'react';
import { Users, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';

export function ParentSignIn() {
  const navigate = useNavigate();
  const { login } = useApp();
  const [email, setEmail] = useState('');
  const [mobile, setMobile] = useState('');
  const [showChildSelect, setShowChildSelect] = useState(false);

  const handleDemoLogin = () => {
    setShowChildSelect(true);
  };

  const handleChildSelect = (childName: string) => {
    login('parent', `Parent of ${childName}`);
    navigate('/parent/dashboard');
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setShowChildSelect(true);
  };

  if (showChildSelect) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-white flex items-center justify-center px-6">
        <div className="w-full max-w-md">
          <button
            onClick={() => setShowChildSelect(false)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-8"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to login
          </button>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-center text-gray-900 mb-6">Select Your Child</h2>

            <div className="space-y-3">
              <button
                onClick={() => handleChildSelect('Emma Rodriguez')}
                className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all text-left"
              >
                <div className="font-medium text-gray-900">Emma Rodriguez</div>
                <div className="text-sm text-gray-600">Grade 7 - Section A</div>
              </button>

              <button
                onClick={() => handleChildSelect('Lucas Rodriguez')}
                className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all text-left"
              >
                <div className="font-medium text-gray-900">Lucas Rodriguez</div>
                <div className="text-sm text-gray-600">Grade 4 - Section B</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-white flex items-center justify-center px-6">
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
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <Users className="w-8 h-8 text-green-600" />
            </div>
          </div>

          <h2 className="text-3xl font-semibold text-center text-gray-900 mb-2">Parent Sign In</h2>
          <p className="text-center text-gray-600 mb-8">Track your child's progress</p>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label htmlFor="parent-email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="parent-email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                placeholder="parent@email.com"
              />
            </div>

            <div>
              <label htmlFor="mobile" className="block text-sm font-medium text-gray-700 mb-2">
                Mobile Number
              </label>
              <input
                type="tel"
                id="mobile"
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                placeholder="+1 (555) 000-0000"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors font-medium"
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
            className="w-full border-2 border-green-600 text-green-600 py-3 rounded-lg hover:bg-green-50 transition-colors font-medium"
          >
            Demo Parent Login
          </button>
        </div>
      </div>
    </div>
  );
}
