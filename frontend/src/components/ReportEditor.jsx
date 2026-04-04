import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { FaTimes, FaDownload, FaSave } from 'react-icons/fa';
import './ReportEditor.css';

const ReportEditor = ({ assignmentId, onClose }) => {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [reportData, setReportData] = useState({
        patient_name: '',
        doctor_name: '',
        patient_age: '',
        patient_gender: '',
        diagnosis: '',
        symptoms: '',
        treatment: '',
        medications: '',
        notes: '',
        exists: false
    });

    useEffect(() => {
        fetchReport();
    }, [assignmentId]);

    const fetchReport = async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/reports/${assignmentId}`);
            const data = await response.json();

            if (data.success) {
                setReportData(data.report);
            }
        } catch (error) {
            toast.error('Failed to load report');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setReportData({
            ...reportData,
            [e.target.name]: e.target.value
        });
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const url = reportData.exists
                ? `http://localhost:8000/api/reports/${assignmentId}`
                : `http://localhost:8000/api/reports/create`;

            const method = reportData.exists ? 'PUT' : 'POST';

            const payload = reportData.exists ? {
                patient_age: reportData.patient_age,
                patient_gender: reportData.patient_gender,
                diagnosis: reportData.diagnosis,
                symptoms: reportData.symptoms,
                treatment: reportData.treatment,
                medications: reportData.medications,
                notes: reportData.notes
            } : {
                assignment_id: assignmentId,
                ...reportData
            };

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                toast.success('Report saved successfully');
                setReportData({ ...reportData, exists: true });
            } else {
                toast.error(data.detail || 'Failed to save report');
            }
        } catch (error) {
            toast.error('Failed to save report');
            console.error(error);
        } finally {
            setSaving(false);
        }
    };

    const handleDownload = async () => {
        if (!reportData.exists) {
            toast.warning('Please save the report first');
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/api/reports/${assignmentId}/download`);

            if (!response.ok) {
                throw new Error('Download failed');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `patient_report_${reportData.patient_name}_${Date.now()}.docx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            toast.success('Report downloaded successfully');
        } catch (error) {
            toast.error('Failed to download report');
            console.error(error);
        }
    };

    if (loading) {
        return (
            <div className="report-editor-overlay">
                <div className="report-editor">
                    <div className="loading-spinner"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="report-editor-overlay" onClick={onClose}>
            <div className="report-editor" onClick={(e) => e.stopPropagation()}>
                <div className="report-header">
                    <h2>Patient Medical Report</h2>
                    <button className="close-btn" onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>

                <div className="report-content">
                    <div className="report-section">
                        <h3>Patient Information</h3>
                        <div className="form-row">
                            <div className="form-group">
                                <label>Patient Name</label>
                                <input
                                    type="text"
                                    value={reportData.patient_name}
                                    disabled
                                    className="form-input"
                                />
                            </div>
                            <div className="form-group">
                                <label>Doctor Name</label>
                                <input
                                    type="text"
                                    value={reportData.doctor_name}
                                    disabled
                                    className="form-input"
                                />
                            </div>
                        </div>
                        <div className="form-row">
                            <div className="form-group">
                                <label>Age</label>
                                <input
                                    type="text"
                                    name="patient_age"
                                    value={reportData.patient_age}
                                    onChange={handleChange}
                                    className="form-input"
                                    placeholder="Enter patient age"
                                />
                            </div>
                            <div className="form-group">
                                <label>Gender</label>
                                <select
                                    name="patient_gender"
                                    value={reportData.patient_gender}
                                    onChange={handleChange}
                                    className="form-input"
                                >
                                    <option value="">Select Gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div className="report-section">
                        <h3>Medical Information</h3>

                        <div className="form-group">
                            <label>Symptoms</label>
                            <textarea
                                name="symptoms"
                                value={reportData.symptoms}
                                onChange={handleChange}
                                className="form-textarea"
                                rows="3"
                                placeholder="Describe patient symptoms..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Diagnosis</label>
                            <textarea
                                name="diagnosis"
                                value={reportData.diagnosis}
                                onChange={handleChange}
                                className="form-textarea"
                                rows="3"
                                placeholder="Enter diagnosis..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Treatment Plan</label>
                            <textarea
                                name="treatment"
                                value={reportData.treatment}
                                onChange={handleChange}
                                className="form-textarea"
                                rows="3"
                                placeholder="Describe treatment plan..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Medications</label>
                            <textarea
                                name="medications"
                                value={reportData.medications}
                                onChange={handleChange}
                                className="form-textarea"
                                rows="3"
                                placeholder="List prescribed medications..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Additional Notes</label>
                            <textarea
                                name="notes"
                                value={reportData.notes}
                                onChange={handleChange}
                                className="form-textarea"
                                rows="3"
                                placeholder="Any additional notes..."
                            />
                        </div>
                    </div>
                </div>

                <div className="report-footer">
                    <button
                        className="btn btn-primary"
                        onClick={handleSave}
                        disabled={saving}
                    >
                        <FaSave /> {saving ? 'Saving...' : 'Save Report'}
                    </button>
                    <button
                        className="btn btn-success"
                        onClick={handleDownload}
                        disabled={!reportData.exists}
                    >
                        <FaDownload /> Download Word Document
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ReportEditor;
