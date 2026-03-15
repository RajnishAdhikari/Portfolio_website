import api from '../lib/axios';

/**
 * Public API service for fetching portfolio data
 * All endpoints are public - no authentication required
 */

export const publicApi = {
    // Personal Info
    async getPersonalInfo() {
        try {
            const response = await api.get('/api/v1/personal');
            return response;
        } catch (error) {
            console.error('Error fetching personal info:', error);
            throw error;
        }
    },

    // Education
    async getEducation() {
        try {
            const response = await api.get('/api/v1/education');
            return response;
        } catch (error) {
            console.error('Error fetching education:', error);
            throw error;
        }
    },

    // Experience
    async getExperience() {
        try {
            const response = await api.get('/api/v1/experience');
            return response;
        } catch (error) {
            console.error('Error fetching experience:', error);
            throw error;
        }
    },

    // Skills
    async getSkills() {
        try {
            const response = await api.get('/api/v1/skills');
            return response;
        } catch (error) {
            console.error('Error fetching skills:', error);
            throw error;
        }
    },

    // Projects
    async getProjects() {
        try {
            const response = await api.get('/api/v1/projects');
            return response;
        } catch (error) {
            console.error('Error fetching projects:', error);
            throw error;
        }
    },

    async getProjectBySlug(slug) {
        try {
            const response = await api.get(`/api/v1/projects/${slug}`);
            return response;
        } catch (error) {
            console.error('Error fetching project:', error);
            throw error;
        }
    },

    // Articles
    async getArticles(params = {}) {
        try {
            const response = await api.get('/api/v1/articles', { params });
            return response;
        } catch (error) {
            console.error('Error fetching articles:', error);
            throw error;
        }
    },

    async getArticleBySlug(slug) {
        try {
            const response = await api.get(`/api/v1/articles/${slug}`);
            return response;
        } catch (error) {
            console.error('Error fetching article:', error);
            throw error;
        }
    },

    // Certifications
    async getCertifications() {
        try {
            const response = await api.get('/api/v1/certifications');
            return response;
        } catch (error) {
            console.error('Error fetching certifications:', error);
            throw error;
        }
    },

    // Extracurricular
    async getExtracurricular() {
        try {
            const response = await api.get('/api/v1/extracurricular');
            return response;
        } catch (error) {
            console.error('Error fetching extracurricular:', error);
            throw error;
        }
    },

    // Resource Papers
    async getResourcePapers(params = {}) {
        try {
            const response = await api.get('/api/v1/resource-papers', { params });
            return response;
        } catch (error) {
            console.error('Error fetching resource papers:', error);
            throw error;
        }
    },

    async getResourcePaperBySlug(slug) {
        try {
            const response = await api.get(`/api/v1/resource-papers/${slug}`);
            return response;
        } catch (error) {
            console.error('Error fetching resource paper:', error);
            throw error;
        }
    }
};

export default publicApi;
