import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

// Public pages
import Home from './pages/public/Home';
import BlogPost from './pages/public/BlogPost';

// Admin pages
import Login from './pages/admin/Login';
import Dashboard from './pages/admin/Dashboard';
import PersonalPage from './pages/admin/PersonalPage';
import EducationPage from './pages/admin/EducationPage';
import ExperiencePage from './pages/admin/ExperiencePage';
import SkillsPage from './pages/admin/SkillsPage';
import ProjectsPage from './pages/admin/ProjectsPage';
import ArticlesPage from './pages/admin/ArticlesPage';
import ResourcePapersPage from './pages/admin/ResourcePapersPage';
import CertificationsPage from './pages/admin/CertificationsPage';
import ExtracurricularPage from './pages/admin/ExtracurricularPage';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="spinner"></div>
            </div>
        );
    }

    return isAuthenticated ? children : <Navigate to="/admin/login" replace />;
};

function App() {
    return (
        <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/blog/:slug" element={<BlogPost />} />

            {/* Admin Auth Route */}
            <Route path="/admin/login" element={<Login />} />

            {/* Protected Admin Routes */}
            <Route
                path="/admin"
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            >
                <Route index element={<Navigate to="/admin/personal" replace />} />
                <Route path="personal" element={<PersonalPage />} />
                <Route path="education" element={<EducationPage />} />
                <Route path="experience" element={<ExperiencePage />} />
                <Route path="skills" element={<SkillsPage />} />
                <Route path="projects" element={<ProjectsPage />} />
                <Route path="articles" element={<ArticlesPage />} />
                <Route path="resource-papers" element={<ResourcePapersPage />} />
                <Route path="certifications" element={<CertificationsPage />} />
                <Route path="extracurricular" element={<ExtracurricularPage />} />
            </Route>

            {/* Catch all - redirect to home */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default App;
