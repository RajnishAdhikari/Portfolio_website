import React, { useState, useRef } from 'react';
import { Upload, X } from 'lucide-react';

const FileUpload = ({
    onFileSelect,
    accept = 'image/*',
    maxSize = 5 * 1024 * 1024, // 5MB default
    currentFile = null,
    onRemove = null,
    label = 'Upload File'
}) => {
    const [dragActive, setDragActive] = useState(false);
    const [preview, setPreview] = useState(null);
    const [error, setError] = useState('');
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const validateFile = (file) => {
        if (file.size > maxSize) {
            setError(`File size must be less than ${maxSize / 1024 / 1024}MB`);
            return false;
        }
        setError('');
        return true;
    };

    const handleFile = (file) => {
        if (!validateFile(file)) return;

        // Create preview for images
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(file);
        }

        onFileSelect(file);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleClick = () => {
        inputRef.current?.click();
    };

    const handleRemove = () => {
        setPreview(null);
        if (inputRef.current) {
            inputRef.current.value = '';
        }
        if (onRemove) {
            onRemove();
        }
    };

    return (
        <div className="w-full">
            <input
                ref={inputRef}
                type="file"
                className="hidden"
                accept={accept}
                onChange={handleChange}
            />

            {(preview || currentFile) ? (
                <div className="relative">
                    {preview ? (
                        <img
                            src={preview}
                            alt="Preview"
                            className="w-full h-48 object-cover rounded-lg border border-gray-300 dark:border-gray-600"
                        />
                    ) : currentFile ? (
                        <div className="w-full h-48 bg-gray-100 dark:bg-gray-800 rounded-lg border border-gray-300 dark:border-gray-600 flex items-center justify-center">
                            <p className="text-gray-600 dark:text-gray-400">{currentFile}</p>
                        </div>
                    ) : null}
                    <button
                        onClick={handleRemove}
                        className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors shadow-lg"
                        type="button"
                    >
                        <X size={16} />
                    </button>
                </div>
            ) : (
                <div
                    className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${dragActive
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={handleClick}
                >
                    <Upload
                        size={48}
                        className="mx-auto mb-4 text-gray-400 dark:text-gray-500"
                    />
                    <p className="text-gray-700 dark:text-gray-300 font-medium mb-1">
                        {label}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        Drag and drop or click to browse
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                        Max size: {maxSize / 1024 / 1024}MB
                    </p>
                </div>
            )}

            {error && (
                <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                    {error}
                </p>
            )}
        </div>
    );
};

export default FileUpload;
