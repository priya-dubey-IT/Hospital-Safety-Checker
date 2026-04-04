import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { FaHospital, FaUserMd, FaUserInjured, FaClipboardCheck, FaTachometerAlt, FaDatabase, FaRobot, FaFileMedical, FaSignOutAlt } from 'react-icons/fa';

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [doctor, setDoctor] = useState(null);

    useEffect(() => {
        // Check for doctor in localStorage on every route change
        const savedDoctor = localStorage.getItem('doctor');
        if (savedDoctor) {
            setDoctor(JSON.parse(savedDoctor));
        } else {
            setDoctor(null);
        }
    }, [location.pathname]);

    const isActive = (path) => {
        return location.pathname === path ? 'active' : '';
    };

    const handleLogout = () => {
        localStorage.removeItem('doctor');
        setDoctor(null);
        navigate('/verification');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-brand">
                    <FaHospital size={28} />
                    Hospital Safety Checker
                </Link>

                <ul className="navbar-menu">
                    <li>
                        <Link to="/registration" className={`navbar-link ${isActive('/registration')}`}>
                            <FaUserMd /> Registration
                        </Link>
                    </li>
                    <li>
                        <Link to="/patient-registration" className={`navbar-link ${isActive('/patient-registration')}`}>
                            <FaUserInjured /> Add Patient
                        </Link>
                    </li>
                    {!doctor ? (
                        <li>
                            <Link to="/verification" className={`navbar-link ${isActive('/verification')}`}>
                                <FaClipboardCheck /> Doctor Login
                            </Link>
                        </li>
                    ) : (
                        <li>
                            <Link to="/doctor-dashboard" className={`navbar-link ${isActive('/doctor-dashboard')}`}>
                                <FaTachometerAlt /> Dr. {doctor.name.split(' ')[0]}'s Dashboard
                            </Link>
                        </li>
                    )}
                    <li>
                        <Link to="/dashboard" className={`navbar-link ${isActive('/dashboard')}`}>
                            <FaTachometerAlt /> Master Dashboard
                        </Link>
                    </li>
                    <li>
                        <Link to="/reports" className={`navbar-link ${isActive('/reports')}`}>
                            <FaFileMedical /> Reports
                        </Link>
                    </li>
                    <li>
                        <Link to="/admin" className={`navbar-link ${isActive('/admin')}`}>
                            <FaDatabase /> Admin
                        </Link>
                    </li>
                    <li>
                        <Link to="/chatbot" className={`navbar-link ${isActive('/chatbot')}`}>
                            <FaRobot /> Chatbot
                        </Link>
                    </li>
                    {doctor && (
                        <li>
                            <button className="navbar-link logout-nav-btn" onClick={handleLogout} style={{ background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}>
                                <FaSignOutAlt /> Logout
                            </button>
                        </li>
                    )}
                </ul>
            </div>
        </nav>
    );
};


export default Navbar;
