import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Upload as UploadIcon } from 'lucide-react';
import { toast } from 'react-toastify';
import AdminLayout from '@/components/AdminLayout';
import DataTable from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import FileUpload from '@/components/FileUpload';
import ConfirmDialog from '@/components/ConfirmDialog';
import LoadingSpinner from '@/components/LoadingSpinner';
import { resolveMediaUrl } from '@/lib/media';
import {
    getEducation,
    createEducation,
    updateEducation,
    deleteEducation,
    uploadEducationLogo
} from '@/services/educationService';

const EducationPage = () => {
    const queryClient = useQueryClient();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [editing, setEditing] = useState(null);
    const [uploading, setUploading] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [formData, setFormData] = useState({
        institution: '',
        degree: '',
        field: '',
        location: '',
        grade: '',
        start_month_year: '',
        end_month_year: '',
        description: ''
    });

    const { data: education, isLoading } = useQuery({
        queryKey: ['education'],
        queryFn: getEducation
    });

    const createMutation = useMutation({
        mutationFn: createEducation,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Education entry created successfully!');
            closeModal();
        },
        onError: (error) => toast.error(error.message || 'Failed to create entry')
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => updateEducation(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Education entry updated successfully!');
            closeModal();
        },
        onError: (error) => toast.error(error.message || 'Failed to update entry')
    });

    const deleteMutation = useMutation({
        mutationFn: deleteEducation,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Education entry deleted successfully!');
        },
        onError: (error) => toast.error(error.message || 'Failed to delete entry')
    });

    const uploadLogoMutation = useMutation({
        mutationFn: ({ id, file }) => uploadEducationLogo(id, file),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Logo uploaded successfully!');
            setIsUploadModalOpen(false);
            setSelectedFile(null);
            setUploading(null);
        },
        onError: (error) => toast.error(error.message || 'Failed to upload logo')
    });

    const openCreateModal = () => {
        setEditing(null);
        setFormData({
            institution: '',
            degree: '',
            field: '',
            location: '',
            grade: '',
            start_month_year: '',
            end_month_year: '',
            description: ''
        });
        setIsModalOpen(true);
    };

    const openEditModal = (item) => {
        setEditing(item);
        setFormData({
            institution: item.institution,
            degree: item.degree,
            field: item.field,
            location: item.location,
            grade: item.grade || '',
            start_month_year: item.start_month_year,
            end_month_year: item.end_month_year || '',
            description: item.description || ''
        });
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setEditing(null);
    };

    const openUploadModal = (item) => {
        setUploading(item);
        setSelectedFile(null);
        setIsUploadModalOpen(true);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (editing) {
            updateMutation.mutate({ id: editing.id, data: formData });
        } else {
            createMutation.mutate(formData);
        }
    };

    const handleUpload = () => {
        if (!selectedFile || !uploading) return;
        uploadLogoMutation.mutate({ id: uploading.id, file: selectedFile });
    };

    const handleDelete = (item) => {
        setDeleting(item);
        setIsDeleteDialogOpen(true);
    };

    const confirmDelete = () => {
        if (deleting) {
            deleteMutation.mutate(deleting.id);
            setDeleting(null);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const columns = [
        {
            key: 'institution',
            label: 'Institution',
            render: (value, row) => (
                <div className="flex items-center gap-3">
                    {row.logo ? (
                        <img src={resolveMediaUrl(row.logo)} alt="" className="w-12 h-12 object-contain rounded" />
                    ) : (
                        <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded" />
                    )}
                    <strong>{value}</strong>
                </div>
            )
        },
        { key: 'degree', label: 'Degree' },
        { key: 'field', label: 'Field' },
        { key: 'start_month_year', label: 'Period', render: (value, row) => `${value} - ${row.end_month_year || 'Present'}` },
        {
            key: 'upload',
            label: 'Logo',
            render: (_, row) => (
                <button
                    onClick={() => openUploadModal(row)}
                    className="flex items-center gap-1 px-3 py-1 text-sm bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:bg-green-200 dark:hover:bg-green-800 transition-colors"
                >
                    <UploadIcon size={14} />
                    Upload
                </button>
            )
        }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Education</h1>
                        <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your education history</p>
                    </div>
                    <button
                        onClick={openCreateModal}
                        className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
                    >
                        <Plus size={20} />
                        Add Education
                    </button>
                </div>

                <DataTable
                    columns={columns}
                    data={education || []}
                    isLoading={isLoading}
                    onEdit={openEditModal}
                    onDelete={handleDelete}
                    emptyMessage="No education entries yet. Add your first entry!"
                />

                <Modal isOpen={isModalOpen} onClose={closeModal} title={editing ? 'Edit Education' : 'Add Education'} size="large">
                    <form onSubmit={handleSubmit}>
                        <FormField label="Institution" name="institution" value={formData.institution} onChange={handleInputChange} required />
                        <FormField label="Degree" name="degree" value={formData.degree} onChange={handleInputChange} required placeholder="e.g., Bachelor of Science" />
                        <FormField label="Field of Study" name="field" value={formData.field} onChange={handleInputChange} required placeholder="e.g., Computer Science" />
                        <FormField label="Location" name="location" value={formData.location} onChange={handleInputChange} required placeholder="City, Country" />
                        <FormField label="Grade/GPA" name="grade" value={formData.grade} onChange={handleInputChange} placeholder="Optional" />
                        <div className="grid grid-cols-2 gap-4">
                            <FormField label="Start Date" name="start_month_year" type="month" value={formData.start_month_year} onChange={handleInputChange} required />
                            <FormField label="End Date" name="end_month_year" type="month" value={formData.end_month_year} onChange={handleInputChange} />
                        </div>
                        <FormField label="Description" name="description" type="textarea" value={formData.description} onChange={handleInputChange} rows={3} />

                        <div className="flex justify-end gap-3 mt-6">
                            <button type="button" onClick={closeModal} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">
                                {createMutation.isPending || updateMutation.isPending ? <LoadingSpinner size="small" /> : editing ? 'Update' : 'Create'}
                            </button>
                        </div>
                    </form>
                </Modal>

                <Modal isOpen={isUploadModalOpen} onClose={() => setIsUploadModalOpen(false)} title="Upload Institution Logo" size="medium">
                    <div className="space-y-4">
                        <p className="text-gray-600 dark:text-gray-400">Upload logo for: <strong>{uploading?.institution}</strong></p>
                        <FileUpload onFileSelect={setSelectedFile} accept="image/*" label="Upload Logo" currentFile={uploading?.logo} />
                        <div className="flex justify-end gap-3 mt-6">
                            <button onClick={() => setIsUploadModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button onClick={handleUpload} disabled={!selectedFile || uploadLogoMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">
                                {uploadLogoMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload'}
                            </button>
                        </div>
                    </div>
                </Modal>

                <ConfirmDialog
                    isOpen={isDeleteDialogOpen}
                    onClose={() => setIsDeleteDialogOpen(false)}
                    onConfirm={confirmDelete}
                    title="Delete Education Entry"
                    message={`Are you sure you want to delete "${deleting?.institution}"?`}
                    confirmText="Delete"
                    type="danger"
                />
            </div>
        </AdminLayout>
    );
};

export default EducationPage;

