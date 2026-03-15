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
    getArticles,
    createArticle,
    updateArticle,
    deleteArticle,
    uploadCoverImage,
    uploadPDF
} from '@/services/articlesService';

const ArticlesPage = () => {
    const queryClient = useQueryClient();

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [uploadType, setUploadType] = useState('cover');
    const [editing, setEditing] = useState(null);
    const [uploading, setUploading] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [formData, setFormData] = useState({
        title: '',
        slug: '',
        excerpt: '',
        body: '',
        external_url: '',
        is_featured: false,
    });

    const { data: articles, isLoading } = useQuery({
        queryKey: ['articles'],
        queryFn: getArticles
    });

    const createMutation = useMutation({
        mutationFn: createArticle,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['articles'] });
            toast.success('Article created!');
            setIsModalOpen(false);
        },
        onError: (e) => toast.error(e.message)
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => updateArticle(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['articles'] });
            toast.success('Article updated!');
            setIsModalOpen(false);
        },
        onError: (e) => toast.error(e.message)
    });

    const deleteMutation = useMutation({
        mutationFn: deleteArticle,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['articles'] });
            toast.success('Article deleted!');
        },
        onError: (e) => toast.error(e.message)
    });

    const uploadMutation = useMutation({
        mutationFn: ({ id, file, type }) => (type === 'cover' ? uploadCoverImage(id, file) : uploadPDF(id, file)),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['articles'] });
            toast.success('File uploaded!');
            setIsUploadModalOpen(false);
            setSelectedFile(null);
            setUploading(null);
        },
        onError: (e) => toast.error(e.message)
    });

    const openCreateModal = () => {
        setEditing(null);
        setFormData({
            title: '',
            slug: '',
            excerpt: '',
            body: '',
            external_url: '',
            is_featured: false,
        });
        setIsModalOpen(true);
    };

    const openEditModal = (item) => {
        setEditing(item);
        setFormData({
            title: item.title || '',
            slug: item.slug || '',
            excerpt: item.excerpt || '',
            body: item.body || '',
            external_url: item.external_url || '',
            is_featured: Boolean(item.is_featured),
        });
        setIsModalOpen(true);
    };

    const openUploadModal = (item, type) => {
        setUploading(item);
        setUploadType(type);
        setSelectedFile(null);
        setIsUploadModalOpen(true);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const payload = {
            ...formData,
            slug: formData.slug?.trim() || undefined,
        };

        if (editing) {
            updateMutation.mutate({ id: editing.id, data: payload });
        } else {
            createMutation.mutate(payload);
        }
    };

    const handleUpload = () => {
        if (selectedFile && uploading) {
            uploadMutation.mutate({ id: uploading.id, file: selectedFile, type: uploadType });
        }
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
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const columns = [
        {
            key: 'cover_image',
            label: 'Cover',
            render: (value) =>
                value ? (
                    <img src={resolveMediaUrl(value)} alt="" className="w-16 h-16 object-cover rounded" />
                ) : (
                    <div className="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded" />
                )
        },
        {
            key: 'title',
            label: 'Title',
            render: (value, row) => (
                <div>
                    <strong>{value}</strong>
                    <div className="text-xs text-gray-500">{row.slug}</div>
                </div>
            )
        },
        {
            key: 'excerpt',
            label: 'Excerpt',
            render: (value) => (value ? `${value.substring(0, 70)}${value.length > 70 ? '...' : ''}` : '-')
        },
        {
            key: 'is_featured',
            label: 'Featured',
            render: (value) =>
                value ? (
                    <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded text-xs">
                        Featured
                    </span>
                ) : (
                    '-'
                )
        },
        {
            key: 'created_at',
            label: 'Created',
            render: (value) => (value ? new Date(value).toLocaleDateString() : '-')
        },
        {
            key: 'upload',
            label: 'Files',
            render: (_, row) => (
                <div className="flex gap-2">
                    <button
                        onClick={() => openUploadModal(row, 'cover')}
                        className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded hover:bg-blue-200 transition-colors"
                    >
                        <UploadIcon size={12} /> Cover
                    </button>
                    <button
                        onClick={() => openUploadModal(row, 'pdf')}
                        className="px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded hover:bg-green-200 transition-colors"
                    >
                        <UploadIcon size={12} /> PDF
                    </button>
                </div>
            )
        }
    ];

    return (
        <AdminLayout>
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Articles</h1>
                        <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your blog articles</p>
                    </div>
                    <button
                        onClick={openCreateModal}
                        className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
                    >
                        <Plus size={20} />
                        Add Article
                    </button>
                </div>

                <DataTable
                    columns={columns}
                    data={articles || []}
                    isLoading={isLoading}
                    onEdit={openEditModal}
                    onDelete={handleDelete}
                    emptyMessage="No articles yet!"
                />

                <Modal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    title={editing ? 'Edit Article' : 'Add Article'}
                    size="large"
                >
                    <form onSubmit={handleSubmit}>
                        <FormField label="Title" name="title" value={formData.title} onChange={handleInputChange} required />
                        <FormField
                            label="Slug (optional)"
                            name="slug"
                            value={formData.slug}
                            onChange={handleInputChange}
                            placeholder="auto-generated-if-empty"
                        />
                        <FormField label="Excerpt" name="excerpt" type="textarea" value={formData.excerpt} onChange={handleInputChange} rows={2} required />
                        <FormField label="Body" name="body" type="textarea" value={formData.body} onChange={handleInputChange} rows={6} />
                        <FormField
                            label="External URL"
                            name="external_url"
                            type="url"
                            value={formData.external_url}
                            onChange={handleInputChange}
                            placeholder="https://..."
                        />
                        <div className="flex items-center gap-2 mb-4">
                            <input
                                type="checkbox"
                                name="is_featured"
                                id="article_is_featured"
                                checked={formData.is_featured}
                                onChange={handleInputChange}
                                className="rounded"
                            />
                            <label htmlFor="article_is_featured" className="text-sm text-gray-700 dark:text-gray-300">
                                Feature this article
                            </label>
                        </div>
                        <div className="flex justify-end gap-3 mt-6">
                            <button
                                type="button"
                                onClick={() => setIsModalOpen(false)}
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
                                ) : editing ? (
                                    'Update'
                                ) : (
                                    'Create'
                                )}
                            </button>
                        </div>
                    </form>
                </Modal>

                <Modal
                    isOpen={isUploadModalOpen}
                    onClose={() => setIsUploadModalOpen(false)}
                    title={`Upload ${uploadType === 'cover' ? 'Cover Image' : 'PDF'}`}
                    size="medium"
                >
                    <div className="space-y-4">
                        <p className="text-gray-600 dark:text-gray-400">
                            Upload {uploadType === 'cover' ? 'cover image' : 'PDF'} for: <strong>{uploading?.title}</strong>
                        </p>
                        <FileUpload
                            onFileSelect={setSelectedFile}
                            accept={uploadType === 'cover' ? 'image/*' : 'application/pdf'}
                            label={`Upload ${uploadType === 'cover' ? 'Cover Image' : 'PDF'}`}
                            currentFile={uploadType === 'cover' ? uploading?.cover_image : uploading?.pdf_attachment}
                        />
                        <div className="flex justify-end gap-3 mt-6">
                            <button
                                onClick={() => setIsUploadModalOpen(false)}
                                className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors font-medium"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleUpload}
                                disabled={!selectedFile || uploadMutation.isPending}
                                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50"
                            >
                                {uploadMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload'}
                            </button>
                        </div>
                    </div>
                </Modal>

                <ConfirmDialog
                    isOpen={isDeleteDialogOpen}
                    onClose={() => setIsDeleteDialogOpen(false)}
                    onConfirm={confirmDelete}
                    title="Delete Article"
                    message={`Are you sure you want to delete "${deleting?.title}"?`}
                    confirmText="Delete"
                    type="danger"
                />
            </div>
        </AdminLayout>
    );
};

export default ArticlesPage;
