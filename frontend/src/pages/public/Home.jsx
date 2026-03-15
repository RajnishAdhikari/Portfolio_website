import React, { useEffect, useState } from 'react';
import { Loader2, AlertCircle } from 'lucide-react';
import publicApi from '../../services/publicApi';
import Hero from '../../components/public/Hero';
import EducationSection from '../../components/public/EducationSection';
import ExperienceSection from '../../components/public/ExperienceSection';
import SkillsSection from '../../components/public/SkillsSection';
import ProjectsSection from '../../components/public/ProjectsSection';
import ArticlesSection from '../../components/public/ArticlesSection';
import CertificationsSection from '../../components/public/CertificationsSection';
import ExtracurricularSection from '../../components/public/ExtracurricularSection';
import ResourcePapersSection from '../../components/public/ResourcePapersSection';
import Footer from '../../components/public/Footer';

const Home = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [data, setData] = useState({
        personal: null,
        education: [],
        experience: [],
        skills: [],
        projects: [],
        articles: [],
        certifications: [],
        extracurricular: [],
        resourcePapers: []
    });

    useEffect(() => {
        const fetchPortfolioData = async () => {
            try {
                setLoading(true);
                setError(null);

                // Fetch all data in parallel with individual error handling
                const [
                    personalRes,
                    educationRes,
                    experienceRes,
                    skillsRes,
                    projectsRes,
                    articlesRes,
                    certificationsRes,
                    extracurricularRes,
                    resourcePapersRes
                ] = await Promise.allSettled([
                    publicApi.getPersonalInfo(),
                    publicApi.getEducation(),
                    publicApi.getExperience(),
                    publicApi.getSkills(),
                    publicApi.getProjects(),
                    publicApi.getArticles(),
                    publicApi.getCertifications(),
                    publicApi.getExtracurricular(),
                    publicApi.getResourcePapers()
                ]);


                setData({
                    personal: personalRes.status === 'fulfilled' ? personalRes.value.data : null,
                    education: educationRes.status === 'fulfilled' ? educationRes.value.data : [],
                    experience: experienceRes.status === 'fulfilled' ? experienceRes.value.data : [],
                    skills: skillsRes.status === 'fulfilled' ? skillsRes.value.data : [],
                    projects: projectsRes.status === 'fulfilled' ? projectsRes.value.data : [],
                    articles: articlesRes.status === 'fulfilled' ? articlesRes.value.data : [],
                    certifications: certificationsRes.status === 'fulfilled' ? certificationsRes.value.data : [],
                    extracurricular: extracurricularRes.status === 'fulfilled' ? extracurricularRes.value.data : [],
                    resourcePapers: resourcePapersRes.status === 'fulfilled' ? resourcePapersRes.value.data : []
                });

                setLoading(false);
            } catch (err) {
                console.error('Error fetching portfolio data:', err);
                setError('Failed to load portfolio data. Please try again later.');
                setLoading(false);
            }
        };

        fetchPortfolioData();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
                    <p className="text-lg text-slate-600 dark:text-slate-400">Loading portfolio...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <div className="text-center px-4">
                    <AlertCircle className="w-16 h-16 text-red-600 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                        Oops! Something went wrong
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 mb-6">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                    >
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    // Check if portfolio has any content
    const hasContent = data.personal ||
        (data.education && data.education.length > 0) ||
        (data.experience && data.experience.length > 0) ||
        (data.skills && data.skills.length > 0) ||
        (data.projects && data.projects.length > 0) ||
        (data.articles && data.articles.length > 0) ||
        (data.certifications && data.certifications.length > 0) ||
        (data.extracurricular && data.extracurricular.length > 0) ||
        (data.resourcePapers && data.resourcePapers.length > 0);

    if (!hasContent) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 flex items-center justify-center">
                <div className="text-center px-4">
                    <h1 className="text-5xl font-bold text-slate-900 dark:text-white mb-6">
                        Portfolio Coming Soon
                    </h1>
                    <p className="text-xl text-slate-700 dark:text-slate-300 mb-8">
                        Content is being added. Please check back later!
                    </p>
                    <p className="text-slate-600 dark:text-slate-400 mb-4">
                        Admin? Login to add content.
                    </p>
                    <a
                        href="/admin/login"
                        className="inline-block px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold shadow-lg hover:shadow-xl"
                    >
                        Go to Admin Dashboard
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-white dark:bg-slate-900">
            <Hero personalInfo={data.personal} />
            <EducationSection education={data.education} />
            <ExperienceSection experience={data.experience} />
            <SkillsSection skills={data.skills} />
            <ProjectsSection projects={data.projects} />
            <ArticlesSection articles={data.articles} />
            <CertificationsSection certifications={data.certifications} />
            <ExtracurricularSection activities={data.extracurricular} />
            <ResourcePapersSection papers={data.resourcePapers} />
            <Footer personalInfo={data.personal} />
        </div>
    );
};

export default Home;
