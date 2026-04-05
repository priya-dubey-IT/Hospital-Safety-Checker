import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { registerPatientOnly, getAllDoctors } from '../services/api';
import { FaUserInjured, FaCheckCircle } from 'react-icons/fa';
import WebcamCapture from '../components/WebcamCapture';
import './Registration.css';

const PatientRegistration = () => {
    const [doctors, setDoctors] = useState([]);
    const [formData, setFormData] = useState({
        doctor_name: '',
        patient_name: '',
        patient_face_image: null
    });

    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        fetchDoctors();
    }, []);

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

    const handlePatientCapture = (imageSrc) => {
        setFormData({
            ...formData,
            patient_face_image: imageSrc
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.doctor_name) {
            toast.error('Please select a doctor');
            return;
        }

        if (!formData.patient_name.trim()) {
            toast.error('Patient name is required');
            return;
        }

        setLoading(true);

        try {
            const response = await registerPatientOnly(formData);

            if (response.success) {
                toast.success('Patient registered successfully!');
                setSuccess(true);

                setTimeout(() => {
                    setFormData({
                        doctor_name: '',
                        patient_name: '',
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
                    <h2>Patient Registered!</h2>
                    <p>Patient has been successfully added to the doctor.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="registration-page">
            <div className="page-header">
                <h1>Patient Registration</h1>
                <p>Add a new patient to an existing doctor</p>
            </div>

            <form onSubmit={handleSubmit} className="registration-form">
                <div className="form-section">
                    <div className="section-header">
                        <FaUserInjured size={24} />
                        <h2>Patient Information</h2>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Select Doctor *</label>
                        <select
                            name="doctor_name"
                            value={formData.doctor_name}
                            onChange={handleInputChange}
                            className="form-select"
                            required
                        >
                            <option value="">Choose a doctor</option>
                            {doctors.map((doctor) => (
                                <option key={doctor.id} value={doctor.name}>
                                    {doctor.name} - {doctor.category}
                                </option>
                            ))}
                        </select>
                        {doctors.length === 0 && (
                            <small className="text-muted">
                                No doctors found. Please register a doctor first.
                            </small>
                        )}
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
                        disabled={loading || doctors.length === 0}
                    >
                        {loading ? 'Registering...' : 'Register Patient'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default PatientRegistration;

