import React, { createContext, useContext, useState, ReactNode } from 'react';

// --- Types ---
export type Role = 'teacher' | 'student' | 'parent' | 'none';

export interface UserSession {
    role: Role;
    userId: string;
    name: string;
}

export interface Student {
    id: string;
    name: string;
    class: string;
    subjects: string[];
    grades: { assignmentId: string; score: number }[];
}

export interface Assignment {
    id: string;
    title: string;
    subject: string;
    totalPoints: number;
    status: 'pending' | 'graded';
}

export interface GradeResult {
    studentId: string;
    assignmentId: string;
    score: number;
    feedback: string;
    weakTopics: string[];
}

interface AppContextType {
    // Session
    user: UserSession | null;
    login: (role: Role, name?: string) => void;
    logout: () => void;

    // Data
    students: Student[];
    assignments: Assignment[];
    grades: GradeResult[];

    // Time Saved
    timeSavedMinutes: number;
    incrementTimeSaved: (minutes: number) => void;

    // AI Actions (Mock)
    gradeAssignment: (assignmentId: string, results: GradeResult[]) => void;
}

// --- Mock Data ---
const MOCK_STUDENTS: Student[] = [
    { id: 's1', name: 'Aryan', class: '10-A', subjects: ['Math', 'Science'], grades: [] },
    { id: 's2', name: 'Emma Rodriguez', class: '10-A', subjects: ['Math', 'Science'], grades: [] },
    { id: 's3', name: 'Marcus Williams', class: '10-A', subjects: ['Math', 'Science'], grades: [] },
];

const MOCK_ASSIGNMENTS: Assignment[] = [
    { id: 'a1', title: 'Algebra Quiz - Chapter 4', subject: 'Math', totalPoints: 100, status: 'pending' },
    { id: 'a2', title: 'Physics Lab Report', subject: 'Science', totalPoints: 50, status: 'pending' },
];

// --- Context ---
const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<UserSession | null>(null);
    const [students] = useState<Student[]>(MOCK_STUDENTS);
    const [assignments, setAssignments] = useState<Assignment[]>(MOCK_ASSIGNMENTS);
    const [grades, setGrades] = useState<GradeResult[]>([]);
    const [timeSavedMinutes, setTimeSavedMinutes] = useState(0);

    const login = (role: Role, name: string = 'User') => {
        // Simple id generation based on role for demo
        const userId = role === 'student' ? 's1' : role === 'parent' ? 'p1' : 't1';
        setUser({ role, userId, name });
    };

    const logout = () => {
        setUser(null);
    };

    const incrementTimeSaved = (minutes: number) => {
        setTimeSavedMinutes((prev) => prev + minutes);
    };

    const gradeAssignment = (assignmentId: string, results: GradeResult[]) => {
        setGrades((prev) => [...prev, ...results]);

        // Update assignment status
        setAssignments((prev) =>
            prev.map(a => a.id === assignmentId ? { ...a, status: 'graded' } : a)
        );
    };

    return (
        <AppContext.Provider value={{
            user,
            login,
            logout,
            students,
            assignments,
            grades,
            timeSavedMinutes,
            incrementTimeSaved,
            gradeAssignment
        }}>
            {children}
        </AppContext.Provider>
    );
}

export function useApp() {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useApp must be used within an AppProvider');
    }
    return context;
}
