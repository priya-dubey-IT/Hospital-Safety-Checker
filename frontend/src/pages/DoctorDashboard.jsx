import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { getDoctorWaitingList, getDoctorCompletedList, markAsComplete, deleteAssignment } from '../services/api';
import { formatDate, timeAgo } from '../utils/helpers';
import LiveTimer from '../components/LiveTimer';
import ReportEditor from '../components/ReportEditor';
import { FaClock, FaCheckCircle, FaUserMd, FaChevronRight, FaNotesMedical } from 'react-icons/fa';
import './Dashboard.css';

const DoctorDashboard = () => {
    const navigate = useNavigate();
    const [doctor, setDoctor] = useState(null);
    const [waitingList, setWaitingList] = useState([]);
    const [completedList, setCompletedList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('waiting');

    // Dual pane state
    const [selectedPatient, setSelectedPatient] = useState(null);

    useEffect(() => {
        const savedDoctor = localStorage.getItem('doctor');
        if (!savedDoctor) {
            toast.warning('Please login first');
            navigate('/verification');
            return;
        }
        const doctorData = JSON.parse(savedDoctor);
        setDoctor(doctorData);
        fetchData(doctorData.id);

        const interval = setInterval(() => fetchData(doctorData.id), 30000);
        return () => clearInterval(interval);
    }, [navigate]);

    const fetchData = async (doctorId) => {
        try {
            const [waitingResponse, completedResponse] = await Promise.all([
                getDoctorWaitingList(doctorId),
                getDoctorCompletedList(doctorId)
            ]);

            if (waitingResponse.success) setWaitingList(waitingResponse.assignments);
            if (completedResponse.success) setCompletedList(completedResponse.assignments);
        } catch (error) {
            toast.error('Failed to fetch dashboard data');
        } finally {
            setLoading(false);
        }
    };

    const handleComplete = async (assignmentId) => {
        try {
            const response = await markAsComplete(assignmentId);
            if (response.success) {
                toast.success('Marked as completed');
                setSelectedPatient(null);
                fetchData(doctor.id);
            }
        } catch (error) {
            toast.error('Failed to update assignment');
        }
    };

    if (loading || !doctor) {
        return (
            <div className="dashboard-layout loading">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    const currentList = activeTab === 'waiting' ? waitingList : completedList;

    return (
        <div className="dashboard-split-layout">
            {/* LEFT PANE: Master Queue */}
            <div className="queue-pane">
                <div className="pane-header">
                    <h2>My Queue</h2>
                    <div className="queue-tabs">
                        <button
                            className={`queue-tab ${activeTab === 'waiting' ? 'active' : ''}`}
                            onClick={() => { setActiveTab('waiting'); setSelectedPatient(null); }}
                        >
                            Waiting ({waitingList.length})
                        </button>
                        <button
                            className={`queue-tab ${activeTab === 'completed' ? 'active' : ''}`}
                            onClick={() => { setActiveTab('completed'); setSelectedPatient(null); }}
                        >
                            Completed ({completedList.length})
                        </button>
                    </div>
                </div>

                <div className="queue-list">
                    {currentList.length === 0 ? (
                        <div className="queue-empty">
                            {activeTab === 'waiting' ? <FaClock /> : <FaCheckCircle />}
                            <p>No {activeTab} patients</p>
                        </div>
                    ) : (
                        currentList.map(appt => (
                            <div
                                key={appt.assignment_id}
                                className={`queue-item ${selectedPatient?.assignment_id === appt.assignment_id ? 'selected' : ''}`}
                                onClick={() => setSelectedPatient(appt)}
                            >
                                <div className="queue-item-header">
                                    <strong>{appt.patient_name}</strong>
                                    <span className={`badge badge-${activeTab === 'waiting' ? 'warning' : 'success'}`}>
                                        {activeTab}
                                    </span>
                                </div>
                                <div className="queue-item-meta">
                                    {activeTab === 'waiting' ? (
                                        <LiveTimer startTime={appt.timestamp} />
                                    ) : (
                                        <span>{timeAgo(appt.timestamp)}</span>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* RIGHT PANE: Detail View */}
            <div className="detail-pane">
                {selectedPatient ? (
                    <div className="patient-detail-card fade-in">
                        <div className="detail-header">
                            <h2>{selectedPatient.patient_name}</h2>
                            <span className="text-muted">Registered: {formatDate(selectedPatient.timestamp)}</span>
                        </div>

                        <div className="detail-actions">
                            {activeTab === 'waiting' && (
                                <button
                                    className="btn btn-success"
                                    onClick={() => handleComplete(selectedPatient.assignment_id)}
                                >
                                    <FaCheckCircle /> Mark as Completed
                                </button>
                            )}
                        </div>

                        <div className="detail-content">
                            <h3><FaNotesMedical /> Medical Report</h3>
                            <div className="report-container">
                                <ReportEditor
                                    assignmentId={selectedPatient.assignment_id}
                                    inline={true}
                                    onClose={() => fetchData(doctor.id)}
                                />
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="detail-empty">
                        <FaUserMd className="empty-icon" />
                        <h3>Select a patient</h3>
                        <p>Choose a patient from the queue to view details and reports.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DoctorDashboard;
