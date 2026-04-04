import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserMd, FaUserInjured, FaClipboardCheck, FaTachometerAlt, FaDatabase, FaRobot, FaShieldAlt } from 'react-icons/fa';
import './Home.css';

const Home = () => {
    const features = [
        {
            icon: <FaUserMd size={40} />,
            title: 'Doctor & Patient Registration',
            description: 'Register doctors and patients with biometric authentication using face recognition and fingerprint.',
            link: '/registration',
            color: '#667eea'
        },
        {
            icon: <FaUserInjured size={40} />,
            title: 'Patient Management',
            description: 'Add new patients to existing doctors quickly and securely with duplicate prevention.',
            link: '/patient-registration',
            color: '#3b82f6'
        },
        {
            icon: <FaClipboardCheck size={40} />,
            title: 'Biometric Verification',
            description: 'Verify doctors using face or fingerprint authentication for secure access.',
            link: '/verification',
            color: '#10b981'
        },
        {
            icon: <FaTachometerAlt size={40} />,
            title: 'Dashboard',
            description: 'Monitor waiting and completed appointments in real-time with intuitive interface.',
            link: '/dashboard',
            color: '#f59e0b'
        },
        {
            icon: <FaDatabase size={40} />,
            title: 'Admin Panel',
            description: 'Manage all data, export to Excel, and maintain complete system control.',
            link: '/admin',
            color: '#8b5cf6'
        },
        {
            icon: <FaRobot size={40} />,
            title: 'AI Chatbot',
            description: 'Get instant answers about hospital workflow, patient info, and system queries.',
            link: '/chatbot',
            color: '#ec4899'
        }
    ];

    return (
        <div className="home-page">
            <div className="hero-section">
                <div className="hero-icon">
                    <FaShieldAlt size={80} />
                </div>
                <h1 className="hero-title">Hospital Safety Checker</h1>
                <p className="hero-subtitle">
                    Professional Biometric Patient Management System
                </p>
                <p className="hero-description">
                    Secure, scalable, and production-ready hospital safety solution with advanced face recognition,
                    fingerprint authentication, and comprehensive patient tracking.
                </p>
                <div className="hero-actions">
                    <Link to="/registration" className="btn btn-primary btn-lg">
                        Get Started
                    </Link>
                    <Link to="/dashboard" className="btn btn-secondary btn-lg">
                        View Dashboard
                    </Link>
                </div>
            </div>

            <div className="features-section">
                <h2 className="section-title">Core Features</h2>
                <div className="features-grid">
                    {features.map((feature, index) => (
                        <Link
                            to={feature.link}
                            key={index}
                            className="feature-card"
                            style={{ '--feature-color': feature.color }}
                        >
                            <div className="feature-icon" style={{ color: feature.color }}>
                                {feature.icon}
                            </div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-description">{feature.description}</p>
                            <div className="feature-arrow">→</div>
                        </Link>
                    ))}
                </div>
            </div>

            <div className="stats-section">
                <div className="stat-card">
                    <div className="stat-number">99.9%</div>
                    <div className="stat-label">Accuracy</div>
                </div>
                <div className="stat-card">
                    <div className="stat-number">24/7</div>
                    <div className="stat-label">Availability</div>
                </div>
                <div className="stat-card">
                    <div className="stat-number">100%</div>
                    <div className="stat-label">Secure</div>
                </div>
                <div className="stat-card">
                    <div className="stat-number">Fast</div>
                    <div className="stat-label">Response Time</div>
                </div>
            </div>
        </div>
    );
};

export default Home;
