import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import AdminLayout from '@/components/AdminLayout';
import FormField from '@/components/FormField';
import FileUpload from '@/components/FileUpload';
import LoadingSpinner from '@/components/LoadingSpinner';
import { getPersonal, updatePersonal, uploadProfilePic, uploadCV } from '@/services/personalService';
import { resolveMediaUrl } from '@/lib/media';

const PersonalPage = () => {
    const queryClient = useQueryClient();
    const [formData, setFormData] = useState({});
    const [profilePicFile, setProfilePicFile] = useState(null);
    const [cvFile, setCVFile] = useState(null);

    const { data: personal, isLoading } = useQuery({
        queryKey: ['personal'],
        queryFn: getPersonal
    });

    // Populate form when data is loaded
    useEffect(() => {
        if (personal) {
            setFormData(personal);
        }
    }, [personal]);

    const updateMutation = useMutation({
        mutationFn: updatePersonal,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Personal info updated!');
        },
        onError: (e) => toast.error(e.message)
    });

    const uploadPicMutation = useMutation({
        mutationFn: uploadProfilePic,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('Profile picture uploaded!');
            setProfilePicFile(null);
        },
        onError: (e) => toast.error(e.message)
    });

    const uploadCVMutation = useMutation({
        mutationFn: uploadCV,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [''] });
            toast.success('CV uploaded!');
            setCVFile(null);
        },
        onError: (e) => toast.error(e.message)
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        updateMutation.mutate(formData);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    if (isLoading) return <AdminLayout><LoadingSpinner size="large" /></AdminLayout>;

    return (
        <AdminLayout>
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Personal Information</h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                        <h2 className="text-xl font-semibold mb-4">Basic Info</h2>
                        <FormField label="Full Name" name="full_name" value={formData.full_name || ''} onChange={handleInputChange} required />
                        <FormField label="Tagline" name="tagline" value={formData.tagline || ''} onChange={handleInputChange} placeholder="Your professional tagline" />
                        <FormField label="Email" name="email" type="email" value={formData.email || ''} onChange={handleInputChange} required />
                        <FormField label="Phone" name="phone" value={formData.phone || ''} onChange={handleInputChange} />
                        <FormField label="Address" name="address" type="textarea" value={formData.address || ''} onChange={handleInputChange} rows={3} placeholder="Your address" />
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                        <h2 className="text-xl font-semibold mb-4">Social Links</h2>
                        <FormField label="LinkedIn" name="linkedin_url" type="url" value={formData.linkedin_url || ''} onChange={handleInputChange} placeholder="https://linkedin.com/in/username" />
                        <FormField label="GitHub" name="github_url" type="url" value={formData.github_url || ''} onChange={handleInputChange} placeholder="https://github.com/username" />
                        <FormField label="Twitter" name="twitter_url" type="url" value={formData.twitter_url || ''} onChange={handleInputChange} placeholder="https://twitter.com/username" />
                    </div>

                    <button type="submit" disabled={updateMutation.isPending} className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50">
                        {updateMutation.isPending ? <LoadingSpinner size="small" /> : 'Save Changes'}
                    </button>
                </form>

                <div className="mt-8 grid grid-cols-2 gap-6">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                        <h2 className="text-xl font-semibold mb-4">Profile Picture</h2>
                        {personal?.profile_pic && (
                            <img src={resolveMediaUrl(personal.profile_pic)} alt="Profile" className="w-32 h-32 rounded-full object-cover mb-4" />
                        )}
                        <FileUpload onFileSelect={setProfilePicFile} accept="image/*" label="Upload Profile Picture" />
                        {profilePicFile && (
                            <button onClick={() => uploadPicMutation.mutate(profilePicFile)} disabled={uploadPicMutation.isPending} className="mt-4 w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50">
                                {uploadPicMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload Picture'}
                            </button>
                        )}
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                        <h2 className="text-xl font-semibold mb-4">CV/Resume</h2>
                        {personal?.cv_file && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Current CV: {personal.cv_file.split('/').pop()}</p>
                        )}
                        <FileUpload onFileSelect={setCVFile} accept=".pdf" label="Upload CV (PDF)" />
                        {cvFile && (
                            <button onClick={() => uploadCVMutation.mutate(cvFile)} disabled={uploadCVMutation.isPending} className="mt-4 w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50">
                                {uploadCVMutation.isPending ? <LoadingSpinner size="small" /> : 'Upload CV'}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </AdminLayout>
    );
};

export default PersonalPage;

