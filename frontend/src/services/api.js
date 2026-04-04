import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Registration API
export const mainRegistration = async (data) => {
    const response = await api.post('/api/registration/main', data);
    return response.data;
};

// Patient API
export const registerPatientOnly = async (data) => {
    const response = await api.post('/api/patient/register', data);
    return response.data;
};

export const getAllDoctors = async () => {
    const response = await api.get('/api/patient/doctors');
    return response.data;
};

// Verification API
export const verifyDoctor = async (data) => {
    const response = await api.post('/api/verification/verify', data);
    return response.data;
};

// Dashboard API
export const getWaitingList = async () => {
    const response = await api.get('/api/dashboard/waiting');
    return response.data;
};

export const getCompletedList = async () => {
    const response = await api.get('/api/dashboard/completed');
    return response.data;
};

export const getDoctorWaitingList = async (doctorId) => {
    const response = await api.get(`/api/dashboard/doctor/${doctorId}/waiting`);
    return response.data;
};

export const getDoctorCompletedList = async (doctorId) => {
    const response = await api.get(`/api/dashboard/doctor/${doctorId}/completed`);
    return response.data;
};

export const markAsComplete = async (assignmentId) => {
    const response = await api.put(`/api/dashboard/complete/${assignmentId}`);
    return response.data;
};

export const deleteAssignment = async (assignmentId) => {
    const response = await api.delete(`/api/dashboard/delete/${assignmentId}`);
    return response.data;
};

// Admin API
export const getAdminDoctors = async () => {
    const response = await api.get('/api/admin/doctors');
    return response.data;
};

export const getAdminPatients = async () => {
    const response = await api.get('/api/admin/patients');
    return response.data;
};

export const getAdminAssignments = async () => {
    const response = await api.get('/api/admin/assignments');
    return response.data;
};

export const deleteDoctor = async (doctorId) => {
    const response = await api.delete(`/api/admin/doctor/${doctorId}`);
    return response.data;
};

export const deletePatient = async (patientId) => {
    const response = await api.delete(`/api/admin/patient/${patientId}`);
    return response.data;
};

export const exportToExcel = async () => {
    const response = await api.get('/api/admin/export/excel', {
        responseType: 'blob',
    });
    return response.data;
};

// Chatbot API
export const sendChatMessage = async (message, sessionId = 'default') => {
    const response = await api.post('/api/chatbot/chat', {
        message,
        session_id: sessionId,
    });
    return response.data;
};

export const getChatHistory = async (sessionId = 'default') => {
    const response = await api.get(`/api/chatbot/history?session_id=${sessionId}`);
    return response.data;
};

// Reports API
export const getReport = async (assignmentId) => {
    const response = await api.get(`/api/reports/${assignmentId}`);
    return response.data;
};

export const createReport = async (data) => {
    const response = await api.post('/api/reports/create', data);
    return response.data;
};

export const updateReport = async (assignmentId, data) => {
    const response = await api.put(`/api/reports/${assignmentId}`, data);
    return response.data;
};

export const downloadReport = async (assignmentId) => {
    const response = await api.get(`/api/reports/${assignmentId}/download`, {
        responseType: 'blob',
    });
    return response.data;
};

export default api;
