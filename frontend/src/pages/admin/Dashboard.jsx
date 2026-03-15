import React from 'react';
import { Outlet } from 'react-router-dom';
import AdminLayout from '@/components/AdminLayout';

const Dashboard = () => {
    return (
        <AdminLayout>
            <Outlet />
        </AdminLayout>
    );
};

export default Dashboard;
