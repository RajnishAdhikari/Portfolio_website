export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');

export const ENDPOINTS = {
    // Auth
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    LOGOUT: '/api/v1/auth/logout',
    REFRESH: '/api/v1/auth/refresh',

    // Personal
    PERSONAL: '/api/v1/personal',
    PERSONAL_UPLOAD_PROFILE: '/api/v1/personal/upload-profile-pic',
    PERSONAL_UPLOAD_CV: '/api/v1/personal/upload-cv',

    // Education
    EDUCATION: '/api/v1/education',
    EDUCATION_UPLOAD_LOGO: (id) => `/api/v1/education/${id}/upload-logo`,

    // Skills
    SKILLS: '/api/v1/skills',

    // Experience
    EXPERIENCE: '/api/v1/experience',
    EXPERIENCE_UPLOAD_LOGO: (id) => `/api/v1/experience/${id}/upload-logo`,

    // Projects
    PROJECTS: '/api/v1/projects',
    PROJECT_BY_SLUG: (slug) => `/api/v1/projects/${slug}`,
    PROJECT_UPLOAD_COVER: (id) => `/api/v1/projects/${id}/upload-cover`,
    PROJECT_UPLOAD_IMAGE: (id) => `/api/v1/projects/${id}/upload-image`,
    PROJECT_UPLOAD_PDF: (id) => `/api/v1/projects/${id}/upload-pdf`,

    // Articles
    ARTICLES: '/api/v1/articles',
    ARTICLE_BY_SLUG: (slug) => `/api/v1/articles/${slug}`,
    ARTICLE_UPLOAD_COVER: (id) => `/api/v1/articles/${id}/upload-cover`,
    ARTICLE_UPLOAD_PDF: (id) => `/api/v1/articles/${id}/upload-pdf`,

    // Resource Papers
    RESOURCE_PAPERS: '/api/v1/resource-papers',
    RESOURCE_PAPER_BY_SLUG: (slug) => `/api/v1/resource-papers/${slug}`,
    RESOURCE_PAPER_UPLOAD_COVER: (id) => `/api/v1/resource-papers/${id}/upload-cover`,
    RESOURCE_PAPER_UPLOAD_PDF: (id) => `/api/v1/resource-papers/${id}/upload-pdf`,

    // Certifications
    CERTIFICATIONS: '/api/v1/certifications',
    CERTIFICATION_UPLOAD_IMAGE: (id) => `/api/v1/certifications/${id}/upload-image`,

    // Extracurricular
    EXTRACURRICULAR: '/api/v1/extracurricular',
    EXTRACURRICULAR_UPLOAD_CERT: (id) => `/api/v1/extracurricular/${id}/upload-certificate`,

    // Health
    HEALTH: '/health',
};
