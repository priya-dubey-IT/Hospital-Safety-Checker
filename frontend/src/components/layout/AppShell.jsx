import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import './AppShell.css';

const AppShell = ({ children }) => {
    const [isSidebarCollapsed, setSidebarCollapsed] = useState(false);

    return (
        <div className={`app-shell ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
            <Sidebar isCollapsed={isSidebarCollapsed} setCollapsed={setSidebarCollapsed} />

            <div className="shell-main">
                <Topbar />
                <main className="shell-content">
                    <div className="page-container">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default AppShell;
