import axios from '@/lib/axios';

// Get all resource papers
export const getResourcePapers = async () => {
    const response = await axios.get('/api/v1/resource-papers');
    return response.data;
};

// Create resource paper
export const createResourcePaper = async (data) => {
    const response = await axios.post('/api/v1/resource-papers', data);
    return response.data;
};

// Update resource paper
export const updateResourcePaper = async (id, data) => {
    const response = await axios.patch(`/api/v1/resource-papers/${id}`, data);
    return response.data;
};

// Delete resource paper
export const deleteResourcePaper = async (id) => {
    const response = await axios.delete(`/api/v1/resource-papers/${id}`);
    return response.data;
};

// Upload cover image
export const uploadResourcePaperCover = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/resource-papers/${id}/upload-cover`,
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
export const uploadResourcePaperPDF = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/resource-papers/${id}/upload-pdf`,
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
export const uploadCoverImage = uploadResourcePaperCover;
export const uploadPDF = uploadResourcePaperPDF;
