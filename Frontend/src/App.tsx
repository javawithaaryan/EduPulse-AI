import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'motion/react';
import { AppProvider, useApp, Role } from './context/AppContext';
import { HomePage } from './components/HomePage';
import { TeacherSignIn } from './components/TeacherSignIn';
import { ParentSignIn } from './components/ParentSignIn';
import { StudentSignIn } from './components/StudentSignIn';
import { TeacherDashboard } from './components/TeacherDashboard';
import { ParentDashboard } from './components/ParentDashboard';
import { StudentLayout } from './components/StudentLayout';
import { AskAITutorPage } from './components/AskAITutorPage';
import { StudentDashboard } from './components/StudentDashboard';
import ConnectionTest from './components/ConnectionTest';

function RequireAuth({ children, role }: { children: JSX.Element; role: Role }) {
  const { user } = useApp();

  if (!user) {
    return <Navigate to="/" replace />;
  }

  if (user.role !== role) {
    // Redirect to correct dashboard if logged in but wrong role
    return <Navigate to={`/${user.role}/dashboard`} replace />;
  }

  return children;
}

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<HomePage />} />
        <Route path="/test" element={<ConnectionTest />} />

        {/* Login Routes */}
        <Route path="/login/teacher" element={<TeacherSignIn />} />
        <Route path="/login/parent" element={<ParentSignIn />} />
        <Route path="/login/student" element={<StudentSignIn />} />

        {/* Protected Dashboards */}
        <Route
          path="/teacher/dashboard"
          element={
            <RequireAuth role="teacher">
              <TeacherDashboard />
            </RequireAuth>
          }
        />
        <Route
          path="/parent/dashboard"
          element={
            <RequireAuth role="parent">
              <ParentDashboard />
            </RequireAuth>
          }
        />
        <Route
          path="/student/dashboard"
          element={
            <RequireAuth role="student">
              <StudentDashboard />
            </RequireAuth>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <AnimatedRoutes />
        </div>
      </BrowserRouter>
    </AppProvider>
  );
}
