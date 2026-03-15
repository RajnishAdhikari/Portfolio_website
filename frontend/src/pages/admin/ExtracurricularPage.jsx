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
import {
    getExtracurricular,
    createExtracurricular,
    updateExtracurricular,
    deleteExtracurricular,
    uploadCertificate
} from '@/services/extracurricularService';

const ExtracurricularPage = () => {
    const queryClient = useQueryClient();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [editing, setEditing] = useState(null);
    const [uploading, setUploading] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [formData, setFormData] = useState({
        title: '', description: '', external_url: ''
    });

    const { data: activities, isLoading } = useQuery({ queryKey: ['extracurricular'], queryFn: getExtracurricular });
    const createMutation = useMutation({ mutationFn: createExtracurricular, onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Activity created!'); setIsModalOpen(false); }, onError: (e) => toast.error(e.message) });
    const updateMutation = useMutation({ mutationFn: ({ id, data }) => updateExtracurricular(id, data), onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Activity updated!'); setIsModalOpen(false); }, onError: (e) => toast.error(e.message) });
    const deleteMutation = useMutation({ mutationFn: deleteExtracurricular, onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Activity deleted!'); }, onError: (e) => toast.error(e.message) });
    const uploadMutation = useMutation({ mutationFn: ({ id, file }) => uploadCertificate(id, file), onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Certificate uploaded!'); setIsUploadModalOpen(false); setSelectedFile(null); setUploading(null); }, onError: (e) => toast.error(e.message) });

    const openCreateModal = () => { setEditing(null); setFormData({ title: '', description: '', external_url: '' }); setIsModalOpen(true); };
    const openEditModal = (item) => { setEditing(item); setFormData({ title: item.title, description: item.description || '', external_url: item.external_url || '' }); setIsModalOpen(true); };
    const openUploadModal = (item) => { setUploading(item); setSelectedFile(null); setIsUploadModalOpen(true); };
    const handleSubmit = (e) => { e.preventDefault(); if (editing) updateMutation.mutate({ id: editing.id, data: formData }); else createMutation.mutate(formData); };
    const handleUpload = () => { if (selectedFile && uploading) uploadMutation.mutate({ id: uploading.id, file: selectedFile }); };
    const handleDelete = (item) => { setDeleting(item); setIsDeleteDialogOpen(true); };
    const confirmDelete = () => { if (deleting) { deleteMutation.mutate(deleting.id); setDeleting(null); } };
    const handleInputChange = (e) => { const { name, value } = e.target; setFormData(prev => ({ ...prev, [name]: value })); };

    const columns = [
        { key: 'title', label: 'Title' },
        { key: 'description', label: 'Description', render: (value) => value ? value.substring(0, 100) + (value.length > 100 ? '...' : '') : '-' },
        { key: 'upload', label: 'Certificate', render: (_, row) => (<button onClick={() => openUploadModal(row)} className="flex items-center gap-1 px-3 py-1 text-sm bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:bg-green-200 dark:hover:bg-green-800 transition-colors"><UploadIcon size={14} />Upload</button>) }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <div><h1 className="text-3xl font-bold text-gray-900 dark:text-white">Extracurricular Activities</h1><p className="text-gray-600 dark:text-gray-400 mt-1">Manage your extracurricular activities</p></div>
                    <button onClick={openCreateModal} className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"><Plus size={20} />Add Activity</button>
                </div>
                <DataTable columns={columns} data={activities || []} isLoading={isLoading} onEdit={openEditModal} onDelete={handleDelete} emptyMessage="No activities yet!" />
                <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editing ? 'Edit Activity' : 'Add Activity'} size="large">
                    <form onSubmit={handleSubmit}>
                        <FormField label="Title" name="title" value={formData.title} onChange={handleInputChange} required placeholder="e.g., Student Council President" />
                        <FormField label="Description" name="description" type="textarea" value={formData.description} onChange={handleInputChange} rows={4} placeholder="Describe your role and achievements..." />
                        <FormField label="External URL" name="external_url" type="url" value={formData.external_url} onChange={handleInputChange} placeholder="https://..." />
                        <div className="flex justify-end gap-3 mt-6">
                            <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{createMutation.isPending || updateMutation.isPending ? <LoadingSpinner size="small" /> : editing ? 'Update' : 'Create'}</button>
                        </div>
                    </form>
                </Modal>
                <Modal isOpen={isUploadModalOpen} onClose={() => setIsUploadModalOpen(false)} title="Upload Certificate" size="medium">
                    <div className="space-y-4">
                        <p className="text-gray-600 dark:text-gray-400">Upload certificate for: <strong>{uploading?.title}</strong></p>
                        <FileUpload onFileSelect={setSelectedFile} accept="image/*,application/pdf" label="Upload Certificate" currentFile={uploading?.certificate_image} />
                        <div className="flex justify-end gap-3 mt-6">
                            <button onClick={() => setIsUploadModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button onClick={handleUpload} disabled={!selectedFile || uploadMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{uploadMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload'}</button>
                        </div>
                    </div>
                </Modal>
                <ConfirmDialog isOpen={isDeleteDialogOpen} onClose={() => setIsDeleteDialogOpen(false)} onConfirm={confirmDelete} title="Delete Activity" message={`Are you sure you want to delete "${deleting?.title}"?`} confirmText="Delete" type="danger" />
            </div>
        </AdminLayout>
    );
};

export default ExtracurricularPage;

