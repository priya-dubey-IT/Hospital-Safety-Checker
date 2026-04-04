import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const useAuth = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
    // Mock JWT decoded state
    // Roles: Admin, Doctor, Receptionist
    const [user, setUser] = useState({
        id: 'usr_1',
        name: 'Dr. John Smith',
        role: 'Admin',
        initials: 'JS'
    });

    const switchRole = (newRole) => {
        const roleMap = {
            'Admin': { id: 'usr_0', name: 'System Admin', initials: 'SA' },
            'Doctor': { id: 'usr_1', name: 'Dr. John Smith', initials: 'JS' },
            'Receptionist': { id: 'usr_2', name: 'Sarah Desk', initials: 'SD' }
        };

        if (roleMap[newRole]) {
            setUser({
                ...roleMap[newRole],
                role: newRole
            });
        }
    };

    return (
        <UserContext.Provider value={{ user, switchRole }}>
            {children}
        </UserContext.Provider>
    );
};

export const PermissionGuard = ({ allowedRoles, children }) => {
    const { user } = useAuth();

    if (!user || !allowedRoles.includes(user.role)) {
        return null; // Do not render if role is not allowed
    }

    return <>{children}</>;
};
