import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth, PermissionGuard } from '../../context/UserContext';
import {
    FaHome,
    FaUserInjured,
    FaUserMd,
    FaClipboardList,
    FaChartBar,
    FaRobot,
    FaBars,
    FaChevronLeft,
    FaHospital
} from 'react-icons/fa';
import './Sidebar.css';

const NavigationConfig = [
    { path: '/', label: 'Home Dashboard', icon: FaHome, roles: ['Admin', 'Doctor', 'Receptionist'] },
    { path: '/registration', label: 'Doctor Registration', icon: FaUserMd, roles: ['Admin', 'Receptionist'] },
    { path: '/patient-registration', label: 'Patient Onboarding', icon: FaUserInjured, roles: ['Admin', 'Receptionist'] },
    { path: '/doctor-dashboard', label: 'Clinical Workflow', icon: FaClipboardList, roles: ['Admin', 'Doctor'] },
    { path: '/reports', label: 'Medical Reports', icon: FaClipboardList, roles: ['Admin', 'Doctor'] },
    { path: '/admin', label: 'System Analytics', icon: FaChartBar, roles: ['Admin'] },
    { path: '/chatbot', label: 'AI Assistant', icon: FaRobot, roles: ['Admin', 'Doctor', 'Receptionist'] }
];

const Sidebar = ({ isCollapsed, setCollapsed }) => {
    const { user } = useAuth();

    return (
        <aside className={`app-sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-header">
                {!isCollapsed && (
                    <div className="brand-logo">
                        <FaHospital className="brand-icon" />
                        <span>SafetyCheck</span>
                    </div>
                )}
                {isCollapsed && <FaHospital className="brand-icon collapsed-logo" />}
                <button
                    className="collapse-btn"
                    onClick={() => setCollapsed(!isCollapsed)}
                    aria-label="Toggle Sidebar"
                >
                    {isCollapsed ? <FaBars /> : <FaChevronLeft />}
                </button>
            </div>

            <div className="sidebar-role-indicator">
                {!isCollapsed && <span className="role-chip">{user.role}</span>}
            </div>

            <nav className="sidebar-nav">
                {NavigationConfig.map((item) => (
                    <PermissionGuard allowedRoles={item.roles} key={item.path}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                        >
                            <item.icon className="nav-icon" />
                            {!isCollapsed && <span className="nav-label">{item.label}</span>}
                        </NavLink>
                    </PermissionGuard>
                ))}
            </nav>
        </aside>
    );
};

export default Sidebar;
