import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { verifyDoctor, getAllDoctors } from '../services/api';
import { FaUserMd, FaHospital } from 'react-icons/fa';
import './Verification.css';

const Verification = () => {
    const navigate = useNavigate();
    const [doctors, setDoctors] = useState([]);
    const [formData, setFormData] = useState({
        doctor_name: ''
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const savedDoctor = localStorage.getItem('doctor');
        if (savedDoctor) {
            navigate('/doctor-dashboard');
        }
        fetchDoctors();
    }, [navigate]);

    const fetchDoctors = async () => {
        try {
            const response = await getAllDoctors();
            if (response.success) {
                setDoctors(response.doctors);
            }
        } catch (error) {
            toast.error('Failed to fetch doctors');
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.doctor_name) {
            toast.error('Please select a doctor');
            return;
        }

        setLoading(true);

        try {
            const response = await verifyDoctor(formData);

            if (response.success) {
                toast.success('Login successful!');
                localStorage.setItem('doctor', JSON.stringify(response.doctor));
                navigate('/doctor-dashboard');
            }
        } catch (error) {
            console.error('Login error:', error);
            let errorMessage = 'Login failed. Please try again.';
            if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail;
            }
            toast.error(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">

                <div className="auth-header">
                    <FaHospital className="auth-brand-icon" />
                    <h1>Clinical Staff Login</h1>
                    <p>Secure portal for authorized personnel</p>
                </div>

                <div className="auth-card">
                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label className="form-label">
                                <FaUserMd className="input-icon-label" />
                                Select Provider Persona
                            </label>
                            <div className="input-with-icon">
                                <select
                                    name="doctor_name"
                                    value={formData.doctor_name}
                                    onChange={handleInputChange}
                                    className="auth-input"
                                    required
                                >
                                    <option value="" disabled>Choose your profile...</option>
                                    {doctors.map((doctor) => (
                                        <option key={doctor.id} value={doctor.name}>
                                            {doctor.name} - {doctor.category}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary btn-block auth-btn"
                            disabled={loading || doctors.length === 0}
                        >
                            {loading ? 'Authenticating...' : 'Access Workspace'}
                        </button>
                    </form>
                </div>

            </div>
        </div>
    );
};

export default Verification;

