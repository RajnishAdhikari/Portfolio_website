import axios from '@/lib/axios';

// Get all skills
export const getSkills = async (category = null) => {
    const params = category ? { category } : {};
    const response = await axios.get('/api/v1/skills', { params });
    return response.data;
};

// Create skill
export const createSkill = async (data) => {
    const response = await axios.post('/api/v1/skills', data);
    return response.data;
};

// Update skill
export const updateSkill = async (id, data) => {
    const response = await axios.patch(`/api/v1/skills/${id}`, data);
    return response.data;
};

// Delete skill
export const deleteSkill = async (id) => {
    const response = await axios.delete(`/api/v1/skills/${id}`);
    return response.data;
};
