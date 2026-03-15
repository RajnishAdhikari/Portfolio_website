import React from 'react';
import { X } from 'lucide-react';

const ImagePreview = ({ src, alt = 'Preview', onRemove, className = '' }) => {
    return (
        <div className={`relative group ${className}`}>
            <img
                src={src}
                alt={alt}
                className="w-full h-48 object-cover rounded-lg border border-gray-300 dark:border-gray-600"
            />
            {onRemove && (
                <button
                    onClick={onRemove}
                    className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-all opacity-0 group-hover:opacity-100 shadow-lg"
                    type="button"
                >
                    <X size={16} />
                </button>
            )}
        </div>
    );
};

export default ImagePreview;
