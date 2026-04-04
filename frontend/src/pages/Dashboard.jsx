import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { getWaitingList, getCompletedList, markAsComplete, deleteAssignment } from '../services/api';
import { formatDate, timeAgo } from '../utils/helpers';
import LiveTimer from '../components/LiveTimer';
import ReportEditor from '../components/ReportEditor';
import { FaClock, FaCheckCircle, FaTrash } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
    const [waitingList, setWaitingList] = useState([]);
    const [completedList, setCompletedList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('waiting');
    const [selectedAssignment, setSelectedAssignment] = useState(null);

    useEffect(() => {
        fetchData();

        // Auto-refresh every 30 seconds
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [waitingResponse, completedResponse] = await Promise.all([
                getWaitingList(),
                getCompletedList()
            ]);

            if (waitingResponse.success) {
                setWaitingList(waitingResponse.assignments);
            }

            if (completedResponse.success) {
                setCompletedList(completedResponse.assignments);
            }
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
                fetchData();
            }
        } catch (error) {
            toast.error('Failed to update assignment');
        }
    };

    const handleDelete = async (assignmentId) => {
        if (!window.confirm('Are you sure you want to delete this assignment?')) {
            return;
        }

        try {
            const response = await deleteAssignment(assignmentId);
            if (response.success) {
                toast.success('Assignment deleted');
                fetchData();
            }
        } catch (error) {
            toast.error('Failed to delete assignment');
        }
    };

    if (loading) {
        return (
            <div className="dashboard-page">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    return (
        <div className="dashboard-page">
            <div className="page-header">
                <h1>Master Dashboard</h1>
                <p>Monitor and manage all patient appointments</p>
            </div>

            <div className="dashboard-stats">
                <div className="stat-card">
                    <div className="stat-icon waiting">
                        <FaClock size={32} />
                    </div>
                    <div className="stat-info">
                        <div className="stat-number">{waitingList.length}</div>
                        <div className="stat-label">Waiting</div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon completed">
                        <FaCheckCircle size={32} />
                    </div>
                    <div className="stat-info">
                        <div className="stat-number">{completedList.length}</div>
                        <div className="stat-label">Completed</div>
                    </div>
                </div>
            </div>

            <div className="dashboard-tabs">
                <button
                    className={`tab-button ${activeTab === 'waiting' ? 'active' : ''}`}
                    onClick={() => setActiveTab('waiting')}
                >
                    <FaClock /> Waiting List ({waitingList.length})
                </button>
                <button
                    className={`tab-button ${activeTab === 'completed' ? 'active' : ''}`}
                    onClick={() => setActiveTab('completed')}
                >
                    <FaCheckCircle /> Completed ({completedList.length})
                </button>
            </div>

            <div className="dashboard-content">
                {activeTab === 'waiting' && (
                    <div className="appointments-list">
                        {waitingList.length === 0 ? (
                            <div className="empty-state">
                                <FaClock size={60} />
                                <h3>No Waiting Appointments</h3>
                                <p>All appointments have been completed or no verifications yet.</p>
                            </div>
                        ) : (
                            <div className="appointments-grid">
                                {waitingList.map((appointment) => (
                                    <div key={appointment.assignment_id} className="appointment-card waiting">
                                        <div className="appointment-header">
                                            <span className="badge badge-warning">Waiting</span>
                                            <div className="appointment-timer">
                                                <LiveTimer startTime={appointment.timestamp} />
                                            </div>
                                        </div>

                                        <div className="appointment-body">
                                            <div className="appointment-info">
                                                <div className="info-row">
                                                    <strong>Doctor:</strong>
                                                    <span>{appointment.doctor_name}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Category:</strong>
                                                    <span>{appointment.doctor_category}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Patient:</strong>
                                                    <span>{appointment.patient_name}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Time:</strong>
                                                    <span>{formatDate(appointment.timestamp)}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="appointment-actions">
                                            <button
                                                className="btn btn-success btn-sm"
                                                onClick={() => handleComplete(appointment.assignment_id)}
                                            >
                                                <FaCheckCircle /> Complete
                                            </button>
                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDelete(appointment.assignment_id)}
                                            >
                                                <FaTrash /> Delete
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'completed' && (
                    <div className="appointments-list">
                        {completedList.length === 0 ? (
                            <div className="empty-state">
                                <FaCheckCircle size={60} />
                                <h3>No Completed Appointments</h3>
                                <p>Completed appointments will appear here.</p>
                            </div>
                        ) : (
                            <div className="appointments-grid">
                                {completedList.map((appointment) => (
                                    <div
                                        key={appointment.assignment_id}
                                        className="appointment-card completed clickable"
                                        onClick={() => setSelectedAssignment(appointment.assignment_id)}
                                    >
                                        <div className="appointment-header">
                                            <span className="badge badge-success">Completed</span>
                                            <span className="appointment-time">{timeAgo(appointment.timestamp)}</span>
                                        </div>

                                        <div className="appointment-body">
                                            <div className="appointment-info">
                                                <div className="info-row">
                                                    <strong>Doctor:</strong>
                                                    <span>{appointment.doctor_name}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Category:</strong>
                                                    <span>{appointment.doctor_category}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Patient:</strong>
                                                    <span>{appointment.patient_name}</span>
                                                </div>
                                                <div className="info-row">
                                                    <strong>Time:</strong>
                                                    <span>{formatDate(appointment.timestamp)}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="appointment-actions" onClick={(e) => e.stopPropagation()}>
                                            <button
                                                className="btn btn-primary btn-sm"
                                                onClick={() => setSelectedAssignment(appointment.assignment_id)}
                                            >
                                                📝 View/Edit Report
                                            </button>
                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDelete(appointment.assignment_id)}
                                            >
                                                <FaTrash /> Delete
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {selectedAssignment && (
                <ReportEditor
                    assignmentId={selectedAssignment}
                    onClose={() => setSelectedAssignment(null)}
                />
            )}
        </div>
    );
};

export default Dashboard;
