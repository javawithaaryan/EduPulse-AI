import { useNavigate, useLocation, Outlet } from 'react-router-dom';
import { motion } from 'motion/react';
import { GraduationCap, LayoutDashboard, MessageSquare, LineChart, LogOut, Settings, BookOpen } from 'lucide-react';
import { useApp } from '../context/AppContext';

export function StudentLayout() {
    const { user, logout } = useApp();
    const navigate = useNavigate();
    const location = useLocation();
    const userName = user?.name || 'Student';

    const menuItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/student/dashboard' },
        { icon: MessageSquare, label: 'Ask AI Tutor', path: '/student/ask-ai' },
        { icon: LineChart, label: 'My Progress', path: '/student/progress' },
        { icon: BookOpen, label: 'Assignments', path: '/student/assignments' },
    ];

    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar - Fixed */}
            <motion.aside
                initial={{ x: -250 }}
                animate={{ x: 0 }}
                className="w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 z-30 flex flex-col"
            >
                <div className="p-6 border-b border-gray-100 flex items-center gap-3">
                    <GraduationCap className="w-8 h-8 text-purple-600" />
                    <span className="text-xl font-bold text-gray-900">EduPulse</span>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    {menuItems.map((item) => {
                        const isActive = location.pathname === item.path;
                        const Icon = item.icon;

                        return (
                            <motion.button
                                key={item.path}
                                whileHover={{ x: 4 }}
                                onClick={() => navigate(item.path)}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${isActive
                                        ? 'bg-purple-50 text-purple-700 font-medium shadow-sm ring-1 ring-purple-100'
                                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                                    }`}
                            >
                                <Icon className={`w-5 h-5 ${isActive ? 'text-purple-600' : 'text-gray-400'}`} />
                                {item.label}
                            </motion.button>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-gray-100">
                    <div className="flex items-center gap-3 px-4 py-3 mb-2">
                        <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-sm font-bold text-purple-700">
                            {userName.charAt(0)}
                        </div>
                        <div className="text-sm">
                            <div className="font-medium text-gray-900">{userName}</div>
                            <div className="text-xs text-gray-500">Grade 7</div>
                        </div>
                    </div>
                    <button
                        onClick={logout}
                        className="w-full flex items-center gap-3 px-4 py-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors text-sm"
                    >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                    </button>
                </div>
            </motion.aside>

            {/* Main Content Area - Offset for Sidebar */}
            <main className="flex-1 ml-64 p-8">
                <Outlet />
            </main>
        </div>
    );
}
