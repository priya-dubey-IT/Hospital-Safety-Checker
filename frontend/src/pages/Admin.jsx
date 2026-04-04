import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import {
    getAdminDoctors,
    getAdminPatients,
    getAdminAssignments,
    deleteDoctor,
    deletePatient,
    exportToExcel
} from '../services/api';
import { formatDate, downloadBlob } from '../utils/helpers';
import { FaUserMd, FaUserInjured, FaLink, FaTrash, FaFileExcel, FaSearch } from 'react-icons/fa';
import './Admin.css';

const Admin = () => {
    const [activeTab, setActiveTab] = useState('doctors');
    const [doctors, setDoctors] = useState([]);
    const [patients, setPatients] = useState([]);
    const [assignments, setAssignments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [doctorsRes, patientsRes, assignmentsRes] = await Promise.all([
                getAdminDoctors(),
                getAdminPatients(),
                getAdminAssignments()
            ]);

            if (doctorsRes.success) setDoctors(doctorsRes.doctors);
            if (patientsRes.success) setPatients(patientsRes.patients);
            if (assignmentsRes.success) setAssignments(assignmentsRes.assignments);
        } catch (error) {
            toast.error('Failed to fetch data');
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteDoctor = async (doctorId, doctorName) => {
        if (!window.confirm(`Delete doctor "${doctorName}"? This will also delete all related assignments.`)) {
            return;
        }

        try {
            await deleteDoctor(doctorId);
            toast.success('Doctor deleted successfully');
            fetchData();
        } catch (error) {
            toast.error('Failed to delete doctor');
        }
    };

    const handleDeletePatient = async (patientId, patientName) => {
        if (!window.confirm(`Delete patient "${patientName}"? This will also delete all related assignments.`)) {
            return;
        }

        try {
            await deletePatient(patientId);
            toast.success('Patient deleted successfully');
            fetchData();
        } catch (error) {
            toast.error('Failed to delete patient');
        }
    };

    const handleExportExcel = async () => {
        try {
            toast.info('Generating Excel file...');
            const blob = await exportToExcel();
            downloadBlob(blob, `hospital_data_${Date.now()}.xlsx`);
            toast.success('Excel file downloaded successfully!');
        } catch (error) {
            toast.error('Failed to export Excel file');
        }
    };

    const filterData = (data, fields) => {
        if (!searchTerm) return data;
        return data.filter(item =>
            fields.some(field =>
                item[field]?.toString().toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    };

    const filteredDoctors = filterData(doctors, ['name', 'category']);
    const filteredPatients = filterData(patients, ['name']);
    const filteredAssignments = filterData(assignments, ['doctor_name', 'patient_name', 'status']);

    if (loading) {
        return (
            <div className="admin-page">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    return (
        <div className="admin-page">
            <div className="page-header">
                <h1>Admin Panel</h1>
                <p>Manage all system data and export reports</p>
            </div>

            <div className="admin-toolbar">
                <div className="search-box">
                    <FaSearch />
                    <input
                        type="text"
                        placeholder="Search..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>

                <button onClick={handleExportExcel} className="btn btn-success">
                    <FaFileExcel /> Export to Excel
                </button>
            </div>

            <div className="admin-tabs">
                <button
                    className={`tab-button ${activeTab === 'doctors' ? 'active' : ''}`}
                    onClick={() => setActiveTab('doctors')}
                >
                    <FaUserMd /> Doctors ({doctors.length})
                </button>
                <button
                    className={`tab-button ${activeTab === 'patients' ? 'active' : ''}`}
                    onClick={() => setActiveTab('patients')}
                >
                    <FaUserInjured /> Patients ({patients.length})
                </button>
                <button
                    className={`tab-button ${activeTab === 'assignments' ? 'active' : ''}`}
                    onClick={() => setActiveTab('assignments')}
                >
                    <FaLink /> Assignments ({assignments.length})
                </button>
            </div>

            <div className="admin-content">
                {activeTab === 'doctors' && (
                    <div className="table-container">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Category</th>
                                    <th>Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredDoctors.map((doctor) => (
                                    <tr key={doctor.id}>
                                        <td>{doctor.name}</td>
                                        <td>{doctor.category}</td>
                                        <td>{formatDate(doctor.created_at)}</td>
                                        <td>
                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDeleteDoctor(doctor.id, doctor.name)}
                                            >
                                                <FaTrash />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {filteredDoctors.length === 0 && (
                            <div className="empty-state">
                                <p>No doctors found</p>
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'patients' && (
                    <div className="table-container">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPatients.map((patient) => (
                                    <tr key={patient.id}>
                                        <td>{patient.name}</td>
                                        <td>{formatDate(patient.created_at)}</td>
                                        <td>
                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() => handleDeletePatient(patient.id, patient.name)}
                                            >
                                                <FaTrash />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {filteredPatients.length === 0 && (
                            <div className="empty-state">
                                <p>No patients found</p>
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'assignments' && (
                    <div className="table-container">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Doctor</th>
                                    <th>Category</th>
                                    <th>Patient</th>
                                    <th>Status</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredAssignments.map((assignment) => (
                                    <tr key={assignment.id}>
                                        <td>{assignment.doctor_name}</td>
                                        <td>{assignment.doctor_category}</td>
                                        <td>{assignment.patient_name}</td>
                                        <td>
                                            <span className={`badge badge-${assignment.status === 'waiting' ? 'warning' : 'success'}`}>
                                                {assignment.status}
                                            </span>
                                        </td>
                                        <td>{formatDate(assignment.timestamp)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {filteredAssignments.length === 0 && (
                            <div className="empty-state">
                                <p>No assignments found</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Admin;
