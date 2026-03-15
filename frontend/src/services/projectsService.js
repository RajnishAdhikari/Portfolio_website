import axios from '@/lib/axios';

// Get all projects
export const getProjects = async () => {
    const response = await axios.get('/api/v1/projects');
    return response.data;
};

// Create project
export const createProject = async (data) => {
    const response = await axios.post('/api/v1/projects', data);
    return response.data;
};

// Update project
export const updateProject = async (id, data) => {
    const response = await axios.patch(`/api/v1/projects/${id}`, data);
    return response.data;
};

// Delete project
export const deleteProject = async (id) => {
    const response = await axios.delete(`/api/v1/projects/${id}`);
    return response.data;
};

// Upload cover image
export const uploadProjectCover = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/projects/${id}/upload-cover`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};

// Upload gallery images (uploads one at a time)
export const uploadProjectGallery = async (id, files) => {
    const uploadPromises = [];

    // Upload each file individually since backend accepts one file at a time
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        const uploadPromise = axios.post(
            `/api/v1/projects/${id}/upload-image`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );
        uploadPromises.push(uploadPromise);
    }

    // Wait for all uploads to complete
    const results = await Promise.all(uploadPromises);
    return results.map(r => r.data);
};

// Upload PDF
export const uploadProjectPDF = async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        `/api/v1/projects/${id}/upload-pdf`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }
    );
    return response.data;
};
