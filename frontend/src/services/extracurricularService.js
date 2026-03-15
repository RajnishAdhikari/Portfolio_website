import axios from '@/lib/axios';

// Get all extracurricular
export const getExtracurricular = async () => {
    const response = await axios.get('/api/v1/extracurricular');
    return response.data;
};

// Create extracurricular
export const createExtracurricular = async (data) => {
    const response = await axios.post('/api/v1/extracurricular', data);
    return response.data;
};

// Update extracurricular
export const updateExtracurricular = async (id, data) => {
    const response = await axios.patch(`/api/v1/extracurricular/${id}`, data);
    return response.data;
};

// Delete extracurricular
export const deleteExtracurricular = async (id) => {
    const response = await axios.delete(`/api/v1/extracurricular/${id}`);
    return response.data;
};

// Upload certificate
export const uploadExtracurricularCertificate = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/extracurricular/${id}/upload-certificate`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};

// Alias for generic naming
export const uploadCertificate = uploadExtracurricularCertificate;
