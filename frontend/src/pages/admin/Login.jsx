import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import axios from '@/lib/axios';
import { ENDPOINTS } from '@/config/api';
import { toast } from 'react-toastify';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setErrorMessage('');

        try {
            const response = await axios.post(ENDPOINTS.LOGIN, { email, password });

            if (response.data.access_token) {
                login(response.data.access_token, response.data.user || { email });
                toast.success('Login successful!');
                navigate('/admin/personal', { replace: true });
            } else {
                const msg = 'Login failed: access token missing in response.';
                setErrorMessage(msg);
                toast.error(msg);
            }
        } catch (error) {
            const msg =
                error.response?.data?.message ||
                error.response?.data?.detail ||
                'Login failed. Please verify your email and password.';
            setErrorMessage(msg);
            toast.error(msg);
            console.error('Login error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-600 to-accent-600">
            <div className="bg-white dark:bg-slate-800 rounded-lg shadow-2xl p-8 w-full max-w-md">
                <h1 className="text-3xl font-bold text-center mb-8 gradient-text">
                    Admin Login
                </h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium mb-2">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input-field"
                            required
                            placeholder="admin@example.com"
                        />
                    </div>

                    <div>
                        <label htmlFor="password" className="block text-sm font-medium mb-2">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input-field"
                            required
                            placeholder="••••••••"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full btn btn-primary disabled:opacity-50"
                    >
                        {isLoading ? <span className="spinner"></span> : 'Login'}
                    </button>
                </form>
                {errorMessage && (
                    <p className="text-center text-sm text-red-500 mt-4">{errorMessage}</p>
                )}

                <p className="text-center text-sm text-slate-600 dark:text-slate-400 mt-6">
                    Note: You need to create an admin account via API first
                </p>
            </div>
        </div>
    );
};

export default Login;
