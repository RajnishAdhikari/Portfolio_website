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
import { getProjects, createProject, updateProject, deleteProject, uploadProjectCover, uploadProjectPDF } from '@/services/projectsService';
import { resolveMediaUrl } from '@/lib/media';

const ProjectsPage = () => {
    const queryClient = useQueryClient();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [uploadType, setUploadType] = useState('cover'); // 'cover' or 'pdf'
    const [editing, setEditing] = useState(null);
    const [uploading, setUploading] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [formData, setFormData] = useState({
        title: '', slug: '', short_desc: '', detailed_desc: '', tech_stack: '', external_url: '', github_url: ''
    });

    const { data: projects, isLoading } = useQuery({ queryKey: ['projects'], queryFn: getProjects });
    const createMutation = useMutation({
        mutationFn: createProject,
        onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Project created!'); closeModal(); },
        onError: (e) => toast.error(e.message)
    });
    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => updateProject(id, data),
        onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Project updated!'); closeModal(); },
        onError: (e) => toast.error(e.message)
    });
    const deleteMutation = useMutation({
        mutationFn: deleteProject,
        onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('Project deleted!'); },
        onError: (e) => toast.error(e.message)
    });
    const uploadMutation = useMutation({
        mutationFn: ({ id, file, type }) => type === 'cover' ? uploadProjectCover(id, file) : uploadProjectPDF(id, file),
        onSuccess: () => { queryClient.invalidateQueries({ queryKey: [''] }); toast.success('File uploaded!'); setIsUploadModalOpen(false); setSelectedFile(null); setUploading(null); },
        onError: (e) => toast.error(e.message)
    });

    const openCreateModal = () => {
        setEditing(null);
        setFormData({ title: '', slug: '', short_desc: '', detailed_desc: '', tech_stack: '', external_url: '', github_url: '' });
        setIsModalOpen(true);
    };

    const openEditModal = (item) => {
        setEditing(item);
        setFormData({
            title: item.title,
            slug: item.slug || '',
            short_desc: item.short_desc,
            detailed_desc: item.detailed_desc || '',
            tech_stack: Array.isArray(item.tech_stack) ? item.tech_stack.join(', ') : (item.tech_stack || ''),
            external_url: item.external_url || '',
            github_url: item.github_url || ''
        });
        setIsModalOpen(true);
    };

    const closeModal = () => { setIsModalOpen(false); setEditing(null); };

    const openUploadModal = (item, type) => {
        setUploading(item);
        setUploadType(type);
        setSelectedFile(null);
        setIsUploadModalOpen(true);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            ...formData,
            slug: formData.slug?.trim() || undefined,
            tech_stack: formData.tech_stack.split(',').map(t => t.trim()).filter(t => t)
        };
        if (editing) updateMutation.mutate({ id: editing.id, data });
        else createMutation.mutate(data);
    };

    const handleUpload = () => {
        if (selectedFile && uploading) uploadMutation.mutate({ id: uploading.id, file: selectedFile, type: uploadType });
    };

    const handleDelete = (item) => { setDeleting(item); setIsDeleteDialogOpen(true); };
    const confirmDelete = () => { if (deleting) { deleteMutation.mutate(deleting.id); setDeleting(null); } };
    const handleInputChange = (e) => { const { name, value } = e.target; setFormData(prev => ({ ...prev, [name]: value })); };

    const columns = [
        {
            key: 'title', label: 'Project', render: (value, row) => (
                <div className="flex items-center gap-3">
                    {row.cover_image ? <img src={resolveMediaUrl(row.cover_image)} alt="" className="w-16 h-16 object-cover rounded" /> : <div className="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded" />}
                    <div>
                        <strong>{value}</strong>
                        <div className="text-xs text-gray-500">{row.slug}</div>
                    </div>
                </div>
            )
        },
        { key: 'short_desc', label: 'Description', render: (value) => value?.substring(0, 50) + '...' },
        {
            key: 'tech_stack',
            label: 'Tech Stack',
            render: (value) => value && Array.isArray(value) ? value.slice(0, 3).join(', ') : ''
        },
        {
            key: 'upload',
            label: 'Files',
            render: (_, row) => (
                <div className="flex gap-2">
                    <button onClick={() => openUploadModal(row, 'cover')} className="flex items-center gap-1 px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors">
                        <UploadIcon size={12} />Cover
                    </button>
                    <button onClick={() => openUploadModal(row, 'pdf')} className="flex items-center gap-1 px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:bg-green-200 dark:hover:bg-green-800 transition-colors">
                        <UploadIcon size={12} />PDF
                    </button>
                </div>
            )
        }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <div><h1 className="text-3xl font-bold text-gray-900 dark:text-white">Projects</h1><p className="text-gray-600 dark:text-gray-400 mt-1">Manage your portfolio projects</p></div>
                    <button onClick={openCreateModal} className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"><Plus size={20} />Add Project</button>
                </div>
                <DataTable columns={columns} data={projects || []} isLoading={isLoading} onEdit={openEditModal} onDelete={handleDelete} emptyMessage="No projects yet!" />

                <Modal isOpen={isModalOpen} onClose={closeModal} title={editing ? 'Edit Project' : 'Add Project'} size="large">
                    <form onSubmit={handleSubmit}>
                        <FormField label="Title" name="title" value={formData.title} onChange={handleInputChange} required />
                        <FormField label="Slug (optional)" name="slug" value={formData.slug} onChange={handleInputChange} placeholder="auto-generated-if-empty" />
                        <FormField label="Short Description" name="short_desc" type="textarea" value={formData.short_desc} onChange={handleInputChange} rows={2} required />
                        <FormField label="Detailed Description" name="detailed_desc" type="textarea" value={formData.detailed_desc} onChange={handleInputChange} rows={4} />
                        <FormField label="Tech Stack (comma-separated)" name="tech_stack" value={formData.tech_stack} onChange={handleInputChange} placeholder="React, Node.js, MongoDB" />
                        <FormField label="Demo URL" name="external_url" type="url" value={formData.external_url} onChange={handleInputChange} placeholder="https://demo.example.com" />
                        <FormField label="GitHub URL" name="github_url" type="url" value={formData.github_url} onChange={handleInputChange} placeholder="https://github.com/username/repo" />
                        <div className="flex justify-end gap-3 mt-6">
                            <button type="button" onClick={closeModal} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{createMutation.isPending || updateMutation.isPending ? <LoadingSpinner size="small" /> : editing ? 'Update' : 'Create'}</button>
                        </div>
                    </form>
                </Modal>

                <Modal isOpen={isUploadModalOpen} onClose={() => setIsUploadModalOpen(false)} title={`Upload ${uploadType === 'cover' ? 'Cover Image' : 'PDF'}`} size="medium">
                    <div className="space-y-4">
                        <p className="text-gray-600 dark:text-gray-400">Upload {uploadType === 'cover' ? 'cover image' : 'PDF'} for: <strong>{uploading?.title}</strong></p>
                        <FileUpload
                            onFileSelect={setSelectedFile}
                            accept={uploadType === 'cover' ? 'image/*' : 'application/pdf'}
                            label={`Upload ${uploadType === 'cover' ? 'Cover Image' : 'PDF'}`}
                            currentFile={uploadType === 'cover' ? uploading?.cover_image : uploading?.pdf_attachment}
                        />
                        <div className="flex justify-end gap-3 mt-6">
                            <button onClick={() => setIsUploadModalOpen(false)} className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium">Cancel</button>
                            <button onClick={handleUpload} disabled={!selectedFile || uploadMutation.isPending} className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">{uploadMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload'}</button>
                        </div>
                    </div>
                </Modal>

                <ConfirmDialog isOpen={isDeleteDialogOpen} onClose={() => setIsDeleteDialogOpen(false)} onConfirm={confirmDelete} title="Delete Project" message={`Are you sure you want to delete "${deleting?.title}"?`} confirmText="Delete" type="danger" />
            </div>
        </AdminLayout>
    );
};

export default ProjectsPage;

