import axios from '@/lib/axios';

// Get all education
export const getEducation = async () => {
    const response = await axios.get('/api/v1/education');
    return response.data;
};

// Create education
export const createEducation = async (data) => {
    const response = await axios.post('/api/v1/education', data);
    return response.data;
};

// Update education
export const updateEducation = async (id, data) => {
    const response = await axios.patch(`/api/v1/education/${id}`, data);
    return response.data;
};

// Delete education
export const deleteEducation = async (id) => {
    const response = await axios.delete(`/api/v1/education/${id}`);
    return response.data;
};

// Upload institution logo
export const uploadEducationLogo = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/education/${id}/upload-logo`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};
