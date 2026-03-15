import { API_BASE_URL } from '@/config/api';

const API_ORIGIN = (API_BASE_URL || '').replace(/\/+$/, '');

export const resolveMediaUrl = (path) => {
    if (!path) return '';

    const normalized = String(path).replace(/\\/g, '/');

    if (/^https?:\/\//i.test(normalized)) {
        return normalized;
    }

    const prefixed = normalized.startsWith('/') ? normalized : `/${normalized}`;

    if (prefixed.startsWith('/uploads/')) {
        return `${API_ORIGIN}${prefixed}`;
    }

    return prefixed;
};
