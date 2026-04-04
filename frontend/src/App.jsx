import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Context Providers
import { ThemeProvider } from './context/ThemeContext';
import { UserProvider } from './context/UserContext';

// Layout
import AppShell from './components/layout/AppShell';

// Global Styles
import './theme/variables.css';
import './index.css';

// Lazy-loaded Pages (Code Splitting)
const Home = React.lazy(() => import('./pages/Home'));
const Registration = React.lazy(() => import('./pages/Registration'));
const PatientRegistration = React.lazy(() => import('./pages/PatientRegistration'));
const Verification = React.lazy(() => import('./pages/Verification'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const DoctorDashboard = React.lazy(() => import('./pages/DoctorDashboard'));
const Reports = React.lazy(() => import('./pages/Reports'));
const Admin = React.lazy(() => import('./pages/Admin'));
const Chatbot = React.lazy(() => import('./pages/Chatbot'));

// Skeleton Loader for Suspense Fallback
const PageSkeleton = () => (
    <div className="flex-center w-full h-full" style={{ minHeight: '60vh', flexDirection: 'column', gap: '1rem' }}>
        <div className="loading-spinner"></div>
        <span className="text-muted">Loading module...</span>
    </div>
);

function App() {
    return (
        <ThemeProvider>
            <UserProvider>
                <Router>
                    <AppShell>
                        <Suspense fallback={<PageSkeleton />}>
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route path="/registration" element={<Registration />} />
                                <Route path="/patient-registration" element={<PatientRegistration />} />
                                <Route path="/verification" element={<Verification />} />
                                <Route path="/dashboard" element={<Dashboard />} />
                                <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
                                <Route path="/reports" element={<Reports />} />
                                <Route path="/admin" element={<Admin />} />
                                <Route path="/chatbot" element={<Chatbot />} />
                            </Routes>
                        </Suspense>
                    </AppShell>
                    <ToastContainer
                        position="bottom-right"
                        autoClose={3000}
                        hideProgressBar={false}
                        newestOnTop={true}
                        closeOnClick
                        rtl={false}
                        pauseOnFocusLoss
                        draggable
                        pauseOnHover
                        theme="colored"
                    />
                </Router>
            </UserProvider>
        </ThemeProvider>
    );
}

export default App;
