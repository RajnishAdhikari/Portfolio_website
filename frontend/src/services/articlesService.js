import axios from '@/lib/axios';

// Get all articles
export const getArticles = async () => {
    const response = await axios.get('/api/v1/articles');
    return response.data;
};

// Create article
export const createArticle = async (data) => {
    const response = await axios.post('/api/v1/articles', data);
    return response.data;
};

// Update article
export const updateArticle = async (id, data) => {
    const response = await axios.patch(`/api/v1/articles/${id}`, data);
    return response.data;
};

// Delete article
export const deleteArticle = async (id) => {
    const response = await axios.delete(`/api/v1/articles/${id}`);
    return response.data;
};

// Upload cover image
export const uploadArticleCover = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/articles/${id}/upload-cover`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};

// Upload PDF
export const uploadArticlePDF = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/articles/${id}/upload-pdf`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};

// Aliases for generic naming
export const uploadCoverImage = uploadArticleCover;
export const uploadPDF = uploadArticlePDF;
