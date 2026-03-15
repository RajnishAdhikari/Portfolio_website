import axios from '@/lib/axios';

// Personal Info Services
export const getPersonal = async () => {
    const response = await axios.get('/api/v1/personal');
    return response.data;
};

export const updatePersonal = async (data) => {
    const response = await axios.patch('/api/v1/personal', data);
    return response.data;
};

export const uploadProfilePic = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('/api/v1/personal/upload-profile-pic', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const uploadCV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('/api/v1/personal/upload-cv', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
