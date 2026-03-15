import axios from '@/lib/axios';

// Get all experience
export const getExperience = async () => {
    const response = await axios.get('/api/v1/experience');
    return response.data;
};

// Create experience
export const createExperience = async (data) => {
    const response = await axios.post('/api/v1/experience', data);
    return response.data;
};

// Update experience
export const updateExperience = async (id, data) => {
    const response = await axios.patch(`/api/v1/experience/${id}`, data);
    return response.data;
};

// Delete experience
export const deleteExperience = async (id) => {
    const response = await axios.delete(`/api/v1/experience/${id}`);
    return response.data;
};

// Upload company logo
export const uploadExperienceLogo = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/experience/${id}/upload-logo`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};
