import axios from '@/lib/axios';

// Get all certifications
export const getCertifications = async () => {
    const response = await axios.get('/api/v1/certifications');
    return response.data;
};

// Create certification
export const createCertification = async (data) => {
    const response = await axios.post('/api/v1/certifications', data);
    return response.data;
};

// Update certification
export const updateCertification = async (id, data) => {
    const response = await axios.patch(`/api/v1/certifications/${id}`, data);
    return response.data;
};

// Delete certification
export const deleteCertification = async (id) => {
    const response = await axios.delete(`/api/v1/certifications/${id}`);
    return response.data;
};

// Upload certificate image
export const uploadCertificateImage = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/certifications/${id}/upload-image`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};
