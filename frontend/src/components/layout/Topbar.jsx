import React from 'react';
import { useAuth } from '../../context/UserContext';
import { useTheme } from '../../context/ThemeContext';
import { FaMoon, FaSun, FaBell, FaUserCircle } from 'react-icons/fa';
import './Topbar.css';

const Topbar = () => {
    const { user, switchRole } = useAuth();
    const { theme, toggleTheme } = useTheme();

    return (
        <header className="app-topbar">
            <div className="topbar-search">
                {/* Placeholder for global patient search */}
                <input
                    type="search"
                    placeholder="Search patient records (MRN, Name)..."
                    className="search-input"
                />
            </div>

            <div className="topbar-actions">
                <div className="system-status">
                    <span className="status-dot"></span>
                    <span className="status-text">API Online</span>
                </div>

                <button className="icon-btn theme-toggle" onClick={toggleTheme} aria-label="Toggle Theme">
                    {theme === 'light' ? <FaMoon /> : <FaSun />}
                </button>

                <button className="icon-btn notification-btn">
                    <FaBell />
                    <span className="notification-badge">3</span>
                </button>

                <div className="user-profile">
                    <div className="avatar">
                        {user.initials}
                    </div>
                    <div className="user-info">
                        <span className="user-name">{user.name}</span>
                        <select
                            className="role-switcher"
                            value={user.role}
                            onChange={(e) => switchRole(e.target.value)}
                        >
                            <option value="Admin">Admin</option>
                            <option value="Doctor">Doctor</option>
                            <option value="Receptionist">Receptionist</option>
                        </select>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Topbar;
