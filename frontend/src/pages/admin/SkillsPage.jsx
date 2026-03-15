import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { toast } from 'react-toastify';
import AdminLayout from '@/components/AdminLayout';
import DataTable from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import ConfirmDialog from '@/components/ConfirmDialog';
import LoadingSpinner from '@/components/LoadingSpinner';
import { getSkills, createSkill, updateSkill, deleteSkill } from '@/services/skillsService';

const SkillsPage = () => {
    const queryClient = useQueryClient();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [editingSkill, setEditingSkill] = useState(null);
    const [deletingSkill, setDeletingSkill] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        category: '',
        level: 1
    });

    // Fetch skills
    const { data: skills, isLoading } = useQuery({
        queryKey: ['skills'],
        queryFn: getSkills
    });

    // Create mutation
    const createMutation = useMutation({
        mutationFn: createSkill,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Skill created successfully!');
            closeModal();
        },
        onError: (error) => {
            toast.error(error.message || 'Failed to create skill');
        }
    });

    // Update mutation
    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => updateSkill(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Skill updated successfully!');
            closeModal();
        },
        onError: (error) => {
            toast.error(error.message || 'Failed to update skill');
        }
    });

    // Delete mutation
    const deleteMutation = useMutation({
        mutationFn: deleteSkill,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Skill deleted successfully!');
        },
        onError: (error) => {
            toast.error(error.message || 'Failed to delete skill');
        }
    });

    const openCreateModal = () => {
        setEditingSkill(null);
        setFormData({
            name: '',
            category: '',
            level: 1
        });
        setIsModalOpen(true);
    };

    const openEditModal = (skill) => {
        setEditingSkill(skill);
        setFormData({
            name: skill.name,
            category: skill.category,
            level: skill.level || 1
        });
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setEditingSkill(null);
        setFormData({
            name: '',
            category: '',
            level: 1
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (editingSkill) {
            updateMutation.mutate({ id: editingSkill.id, data: formData });
        } else {
            createMutation.mutate(formData);
        }
    };

    const handleDelete = (skill) => {
        setDeletingSkill(skill);
        setIsDeleteDialogOpen(true);
    };

    const confirmDelete = () => {
        if (deletingSkill) {
            deleteMutation.mutate(deletingSkill.id);
            setDeletingSkill(null);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const columns = [
        {
            key: 'name',
            label: 'Skill Name'
        },
        {
            key: 'category',
            label: 'Category',
            render: (value) => (
                <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm">
                    {value}
                </span>
            )
        },
        {
            key: 'level',
            label: 'Level',
            render: (value) => {
                const stars = 'â­'.repeat(value || 0);
                return <span className="text-yellow-500">{stars} ({value}/5)</span>;
            }
        }
    ];

    // Backend expects these exact enum values
    const categoryOptions = [
        { value: 'Frontend', label: 'Frontend' },
        { value: 'Backend', label: 'Backend' },
        { value: 'Language', label: 'Language' },
        { value: 'Tool', label: 'Tool' },
        { value: 'Other', label: 'Other' }
    ];

    // Backend expects numeric level 1-5
    const levelOptions = [
        { value: 1, label: 'â­ Beginner (1)' },
        { value: 2, label: 'â­â­ Novice (2)' },
        { value: 3, label: 'â­â­â­ Intermediate (3)' },
        { value: 4, label: 'â­â­â­â­ Advanced (4)' },
        { value: 5, label: 'â­â­â­â­â­ Expert (5)' }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                            Skills
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400 mt-1">
                            Manage your skills and proficiency levels
                        </p>
                    </div>
                    <button
                        onClick={openCreateModal}
                        className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
                    >
                        <Plus size={20} />
                        Add New Skill
                    </button>
                </div>

                {/* Table */}
                <DataTable
                    columns={columns}
                    data={skills || []}
                    isLoading={isLoading}
                    onEdit={openEditModal}
                    onDelete={handleDelete}
                    emptyMessage="No skills added yet. Add your first skill!"
                />

                {/* Create/Edit Modal */}
                <Modal
                    isOpen={isModalOpen}
                    onClose={closeModal}
                    title={editingSkill ? 'Edit Skill' : 'Add New Skill'}
                    size="medium"
                >
                    <form onSubmit={handleSubmit}>
                        <FormField
                            label="Skill Name"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                            placeholder="e.g., React, Python, Communication"
                        />

                        <FormField
                            label="Category"
                            name="category"
                            type="select"
                            value={formData.category}
                            onChange={handleInputChange}
                            options={categoryOptions}
                            required
                        />

                        <FormField
                            label="Skill Level (1-5)"
                            name="level"
                            type="select"
                            value={formData.level}
                            onChange={handleInputChange}
                            options={levelOptions}
                            required
                        />

                        <div className="flex justify-end gap-3 mt-6">
                            <button
                                type="button"
                                onClick={closeModal}
                                className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={createMutation.isPending || updateMutation.isPending}
                                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50"
                            >
                                {createMutation.isPending || updateMutation.isPending ? (
                                    <LoadingSpinner size="small" />
                                ) : editingSkill ? (
                                    'Update Skill'
                                ) : (
                                    'Create Skill'
                                )}
                            </button>
                        </div>
                    </form>
                </Modal>

                {/* Delete Confirmation */}
                <ConfirmDialog
                    isOpen={isDeleteDialogOpen}
                    onClose={() => setIsDeleteDialogOpen(false)}
                    onConfirm={confirmDelete}
                    title="Delete Skill"
                    message={`Are you sure you want to delete "${deletingSkill?.name}"? This action cannot be undone.`}
                    confirmText="Delete"
                    type="danger"
                />
            </div>
        </AdminLayout>
    );
};

export default SkillsPage;

