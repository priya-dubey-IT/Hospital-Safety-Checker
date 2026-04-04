import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { getCompletedList, downloadReport } from '../services/api';
import { formatDate, downloadBlob } from '../utils/helpers';
import { FaFileMedical, FaDownload, FaSearch, FaUserInjured, FaUserMd } from 'react-icons/fa';
import ReportEditor from '../components/ReportEditor';
import './Reports.css';

const Reports = () => {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedAssignment, setSelectedAssignment] = useState(null);

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        setLoading(true);
        try {
            const response = await getCompletedList();
            if (response.success) {
                setReports(response.assignments);
            }
        } catch (error) {
            toast.error('Failed to fetch reports list');
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = async (assignmentId, patientName) => {
        try {
            toast.info('Downloading report...');
            const blob = await downloadReport(assignmentId);
            downloadBlob(blob, `report_${patientName.replace(/\s+/g, '_')}_${Date.now()}.docx`);
            toast.success('Report downloaded successfully');
        } catch (error) {
            toast.error('Failed to download report. Make sure it has been created.');
        }
    };

    const filteredReports = reports.filter(report =>
        report.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.doctor_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {
        return (
            <div className="reports-page">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    return (
        <div className="reports-page">
            <div className="page-header">
                <h1>Patient Reports</h1>
                <p>View and download medical reports for completed appointments</p>
            </div>

            <div className="reports-toolbar">
                <div className="search-box">
                    <FaSearch />
                    <input
                        type="text"
                        placeholder="Search by patient or doctor name..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>
            </div>

            <div className="reports-grid">
                {filteredReports.length === 0 ? (
                    <div className="empty-state">
                        <FaFileMedical size={64} />
                        <h3>No Reports Found</h3>
                        <p>Completed appointments with reports will appear here.</p>
                    </div>
                ) : (
                    filteredReports.map((report) => (
                        <div key={report.assignment_id} className="report-card">
                            <div className="report-card-header">
                                <div className="patient-info">
                                    <FaUserInjured size={20} />
                                    <span>{report.patient_name}</span>
                                </div>
                                <span className="report-date">{formatDate(report.timestamp)}</span>
                            </div>

                            <div className="report-card-body">
                                <div className="info-item">
                                    <FaUserMd />
                                    <label>Doctor:</label>
                                    <span>{report.doctor_name} ({report.doctor_category})</span>
                                </div>
                                <div className="status-badge">
                                    <span className="badge badge-success">Completed</span>
                                </div>
                            </div>

                            <div className="report-card-actions">
                                <button
                                    className="btn btn-primary btn-sm"
                                    onClick={() => setSelectedAssignment(report.assignment_id)}
                                >
                                    📝 View/Edit Report
                                </button>
                                <button
                                    className="btn btn-success btn-sm"
                                    onClick={() => handleDownload(report.assignment_id, report.patient_name)}
                                >
                                    <FaDownload /> Download
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {selectedAssignment && (
                <ReportEditor
                    assignmentId={selectedAssignment}
                    onClose={() => {
                        setSelectedAssignment(null);
                        fetchReports(); // Refresh in case changes were made
                    }}
                />
            )}
        </div>
    );
};

export default Reports;
