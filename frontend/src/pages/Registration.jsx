import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { mainRegistration } from '../services/api';
import { FaUserMd, FaUserInjured, FaCheckCircle } from 'react-icons/fa';
import WebcamCapture from '../components/WebcamCapture';
import './Registration.css';

const Registration = () => {
    const [formData, setFormData] = useState({
        doctor_name: '',
        doctor_category: '',
        patient_name: '',
        doctor_face_image: null,
        patient_face_image: null
    });

    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const categories = [
        'Cardiologist',
        'Orthopedic',
        'Neurologist',
        'Pediatrician',
        'Dermatologist',
        'General Physician',
        'Surgeon',
        'Psychiatrist',
        'Other'
    ];

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleDoctorCapture = (imageSrc) => {
        setFormData({
            ...formData,
            doctor_face_image: imageSrc
        });
    };

    const handlePatientCapture = (imageSrc) => {
        setFormData({
            ...formData,
            patient_face_image: imageSrc
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validation
        if (!formData.doctor_name.trim()) {
            toast.error('Doctor name is required');
            return;
        }

        if (!formData.doctor_category) {
            toast.error('Doctor category is required');
            return;
        }

        if (!formData.patient_name.trim()) {
            toast.error('Patient name is required');
            return;
        }

        // Biometric check is optional, but encouraged
        if (!formData.doctor_face_image) {
            toast.warning('No face captured for doctor. Proceeding with name only.');
        }

        if (!formData.patient_face_image) {
            toast.warning('No face captured for patient. Proceeding with name only.');
        }

        setLoading(true);

        try {
            const response = await mainRegistration(formData);

            if (response.success) {
                toast.success('Registration successful!');
                setSuccess(true);

                // Reset form after 3 seconds
                setTimeout(() => {
                    setFormData({
                        doctor_name: '',
                        doctor_category: '',
                        patient_name: '',
                        doctor_face_image: null,
                        patient_face_image: null
                    });
                    setSuccess(false);
                }, 3000);
            }
        } catch (error) {
            console.error('Registration error:', error);
            let errorMessage = 'Registration failed. Please try again.';
            if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail;
            }
            toast.error(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="registration-page">
                <div className="success-message">
                    <FaCheckCircle size={80} className="success-icon" />
                    <h2>Registration Successful!</h2>
                    <p>Doctor and patient have been registered successfully.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="registration-page">
            <div className="page-header">
                <h1>Registration</h1>
                <p>Register both doctor and patient together</p>
            </div>

            <form onSubmit={handleSubmit} className="registration-form">
                <div className="form-section">
                    <div className="section-header">
                        <FaUserMd size={24} />
                        <h2>Doctor Information</h2>
                    </div>

                    <div className="form-grid">
                        <div className="form-group">
                            <label className="form-label">Doctor Name *</label>
                            <input
                                type="text"
                                name="doctor_name"
                                value={formData.doctor_name}
                                onChange={handleInputChange}
                                className="form-input"
                                placeholder="Enter doctor's full name"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">Category *</label>
                            <select
                                name="doctor_category"
                                value={formData.doctor_category}
                                onChange={handleInputChange}
                                className="form-select"
                                required
                            >
                                <option value="">Select category</option>
                                {categories.map((cat, index) => (
                                    <option key={index} value={cat}>{cat}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Biometric section disabled for healthcare compliance */}
                    {/* 
                    <div className="biometric-section">
                        <WebcamCapture 
                            onCapture={handleDoctorCapture} 
                            label="Doctor's Face Capture (Optional but recommended)" 
                        />
                    </div>
                    */}
                </div>

                <div className="form-section">
                    <div className="section-header">
                        <FaUserInjured size={24} />
                        <h2>Patient Information</h2>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Patient Name *</label>
                        <input
                            type="text"
                            name="patient_name"
                            value={formData.patient_name}
                            onChange={handleInputChange}
                            className="form-input"
                            placeholder="Enter patient's full name"
                            required
                        />
                    </div>

                    {/* Biometric section disabled for healthcare compliance */}
                    {/* 
                    <div className="biometric-section">
                        <WebcamCapture 
                            onCapture={handlePatientCapture} 
                            label="Patient's Face Capture (Optional)" 
                        />
                    </div>
                    */}
                </div>

                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary btn-lg"
                        disabled={loading}
                    >
                        {loading ? 'Registering...' : 'Register Both'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Registration;
