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
    getCertifications,
    createCertification,
    updateCertification,
    deleteCertification,
    uploadCertificateImage
} from '@/services/certificationsService';

const CertificationsPage = () => {
    const queryClient = useQueryClient();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [editingCert, setEditingCert] = useState(null);
    const [uploadingCert, setUploadingCert] = useState(null);
    const [deletingCert, setDeletingCert] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [formData, setFormData] = useState({
        name: '', issuer: '', issue_month_year: '', cred_id: '', cred_url: '', description: ''
    });

    const { data: certifications, isLoading } = useQuery({ queryKey: ['certifications'], queryFn: getCertifications });
    const createMutation = useMutation({ mutationFn: createCertification, onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Certification created!'); setIsModalOpen(false); }, onError: (e) => toast.error(e.message) });
    const updateMutation = useMutation({ mutationFn: ({ id, data }) => updateCertification(id, data), onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Certification updated!'); setIsModalOpen(false); }, onError: (e) => toast.error(e.message) });
    const deleteMutation = useMutation({ mutationFn: deleteCertification, onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Certification deleted!'); }, onError: (e) => toast.error(e.message) });
    const uploadMutation = useMutation({ mutationFn: ({ id, file }) => uploadCertificateImage(id, file), onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Image uploaded!'); setIsUploadModalOpen(false); setSelectedFile(null); setUploadingCert(null); }, onError: (e) => toast.error(e.message) });

    const openCreateModal = () => { setEditingCert(null); setFormData({ name: '', issuer: '', issue_month_year: '', cred_id: '', cred_url: '', description: '' }); setIsModalOpen(true); };
    const openEditModal = (cert) => { setEditingCert(cert); setFormData({ name: cert.name, issuer: cert.issuer, issue_month_year: cert.issue_month_year, cred_id: cert.cred_id || '', cred_url: cert.cred_url || '', description: cert.description || '' }); setIsModalOpen(true); };
    const openUploadModal = (cert) => { setUploadingCert(cert); setSelectedFile(null); setIsUploadModalOpen(true); };
    const handleSubmit = (e) => { e.preventDefault(); if (editingCert) updateMutation.mutate({ id: editingCert.id, data: formData }); else createMutation.mutate(formData); };
    const handleUpload = () => { if (selectedFile && uploadingCert) uploadMutation.mutate({ id: uploadingCert.id, file: selectedFile }); };
    const handleDelete = (cert) => { setDeletingCert(cert); setIsDeleteDialogOpen(true); };
    const confirmDelete = () => { if (deletingCert) { deleteMutation.mutate(deletingCert.id); setDeletingCert(null); } };
    const handleInputChange = (e) => { const { name, value } = e.target; setFormData(prev => ({ ...prev, [name]: value })); };

    const columns = [
        { key: 'image', label: 'Image', render: (value) => value ? <img src={resolveMediaUrl(value)} alt="Certificate" className="w-16 h-16 object-cover rounded border" /> : <div className="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded border flex items-center justify-center"><span className="text-xs text-gray-400">No image</span></div> },
        { key: 'name', label: 'Certification Name' },
        { key: 'issuer', label: 'Issuer' },
        { key: 'issue_month_year', label: 'Issue Date' },
        { key: 'upload', label: 'Actions', render: (_, row) => (<button onClick={() => openUploadModal(row)} className="flex items-center gap-1 px-3 py-1 text-sm bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:bg-green-200 dark:hover:bg-green-800 transition-colors"><UploadIcon size={14} />Upload Image</button>) }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <div><h1 className="text-3xl font-bold text-gray-900 dark:text-white">Certifications</h1><p className="text-gray-600 dark:text-gray-400 mt-1">Manage your certifications and achievements</p></div>
                    <button onClick={openCreateModal} className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"><Plus size={20} />Add New Certification</button>
                </div>
                <DataTable columns={columns} data={certifications || []} isLoading={isLoading} onEdit={openEditModal} onDelete={handleDelete} emptyMessage="No certifications added yet. Add your first certification!" />
                <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingCert ? 'Edit Certification' : 'Add New Certification'} size="large">
                    <form onSubmit={handleSubmit}>
                        <FormField label="Certification Name" name="name" value={formData.name} onChange={handleInputChange} required placeholder="e.g., AWS Solutions Architect" />
                        <FormField label="Issuer" name="issuer" value={formData.issuer} onChange={handleInputChange} required placeholder="e.g., Amazon Web Services" />
                        <FormField label="Issue Date (YYYY-MM)" name="issue_month_year" type="month" value={formData.issue_month_year} onChange={handleInputChange} required />
                        <FormField label="Credential ID" name="cred_id" value={formData.cred_id} onChange={handleInputChange} placeholder="Optional" />
                        <FormField label="Credential URL" name="cred_url" type="url" value={formData.cred_url} onChange={handleInputChange} placeholder="https://..." />
                        <FormField label="Description" name="description" type="textarea" value={formData.description} onChange={handleInputChange} rows={3} placeholder="Brief description..." />
                        <div className="flex justify-end gap-3 mt-6">
                            <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{createMutation.isPending || updateMutation.isPending ? <LoadingSpinner size="small" /> : editingCert ? 'Update Certification' : 'Create Certification'}</button>
                        </div>
                    </form>
                </Modal>
                <Modal isOpen={isUploadModalOpen} onClose={() => setIsUploadModalOpen(false)} title="Upload Certificate Image" size="medium">
                    <div className="space-y-4">
                        <p className="text-gray-600 dark:text-gray-400">Upload image for: <strong>{uploadingCert?.name}</strong></p>
                        <FileUpload onFileSelect={setSelectedFile} accept="image/*" label="Upload Certificate Image" currentFile={uploadingCert?.image} />
                        <div className="flex justify-end gap-3 mt-6">
                            <button onClick={() => setIsUploadModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button onClick={handleUpload} disabled={!selectedFile || uploadMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{uploadMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload Image'}</button>
                        </div>
                    </div>
                </Modal>
                <ConfirmDialog isOpen={isDeleteDialogOpen} onClose={() => setIsDeleteDialogOpen(false)} onConfirm={confirmDelete} title="Delete Certification" message={`Are you sure you want to delete "${deletingCert?.name}"?`} confirmText="Delete" type="danger" />
            </div>
        </AdminLayout>
    );
};

export default CertificationsPage;

