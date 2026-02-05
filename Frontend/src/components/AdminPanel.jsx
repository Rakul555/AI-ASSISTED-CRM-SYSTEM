import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import ChartSection from './ChartSection';
import ReportDisplay from './ReportDisplay';
import './AdminPanel.css';

const AdminPanel = () => {
    const [loading, setLoading] = useState(false);
    const [reportData, setReportData] = useState(null);
    const [chartsData, setChartsData] = useState(null);
    const [error, setError] = useState(null);
    const [pdfGenerating, setPdfGenerating] = useState(false);
    const [theme, setTheme] = useState(() => {
        // Get theme from localStorage or default to 'light'
        return localStorage.getItem('theme') || 'light';
    });

    // Apply theme on mount and when it changes
    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    };

    const handleGenerateReport = async () => {
        setLoading(true);
        setError(null);

        try {
            // Fetch charts data
            const chartsResponse = await api.getChartsData();
            setChartsData(chartsResponse.data);

            // Generate report
            const reportResponse = await api.generateReport();
            setReportData(reportResponse);

        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate report. Please try again.');
            console.error('Error generating report:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async () => {
        setPdfGenerating(true);

        try {
            const response = await api.generatePDF();

            if (response.status === 'success') {
                // Download the PDF
                api.downloadPDF(response.filename);

                // Show success message
                const successMsg = document.createElement('div');
                successMsg.className = 'success-toast';
                successMsg.textContent = 'PDF downloaded successfully!';
                document.body.appendChild(successMsg);

                setTimeout(() => {
                    document.body.removeChild(successMsg);
                }, 3000);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate PDF. Please try again.');
            console.error('Error generating PDF:', err);
        } finally {
            setPdfGenerating(false);
        }
    };

    return (
        <div className="admin-panel">
            {/* Header */}
            <header className="admin-header">
                <div className="header-content">
                    <div className="title-section">
                        <h1 className="main-title">CRM Analytics Dashboard</h1>
                        <p className="subtitle">AI-Powered Customer Feedback Analysis</p>
                    </div>
                    <div className="header-actions">
                        <button
                            className="theme-toggle"
                            onClick={toggleTheme}
                            aria-label="Toggle theme"
                            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                        >
                            {theme === 'light' ? (
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                                </svg>
                            ) : (
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <circle cx="12" cy="12" r="5"></circle>
                                    <line x1="12" y1="1" x2="12" y2="3"></line>
                                    <line x1="12" y1="21" x2="12" y2="23"></line>
                                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                                    <line x1="1" y1="12" x2="3" y2="12"></line>
                                    <line x1="21" y1="12" x2="23" y2="12"></line>
                                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                                </svg>
                            )}
                        </button>

                        <button
                            className="btn btn-primary"
                            onClick={handleGenerateReport}
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner-small"></span>
                                    Generating...
                                </>
                            ) : (
                                <>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="7 10 12 15 17 10"></polyline>
                                        <line x1="12" y1="15" x2="12" y2="3"></line>
                                    </svg>
                                    Generate Report
                                </>
                            )}
                        </button>

                        {reportData && (
                            <button
                                className="btn btn-secondary"
                                onClick={handleDownloadPDF}
                                disabled={pdfGenerating}
                            >
                                {pdfGenerating ? (
                                    <>
                                        <span className="spinner-small"></span>
                                        Creating PDF...
                                    </>
                                ) : (
                                    <>
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                            <polyline points="14 2 14 8 20 8"></polyline>
                                            <line x1="16" y1="13" x2="8" y2="13"></line>
                                            <line x1="16" y1="17" x2="8" y2="17"></line>
                                            <polyline points="10 9 9 9 8 9"></polyline>
                                        </svg>
                                        Download PDF
                                    </>
                                )}
                            </button>
                        )}
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="admin-content">
                {error && (
                    <div className="error-message card">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        <span>{error}</span>
                    </div>
                )}

                {loading && (
                    <div className="loading-container">
                        <div className="spinner"></div>
                        <p className="loading-text">Analyzing data and generating insights...</p>
                    </div>
                )}

                {!loading && !reportData && !error && (
                    <div className="empty-state card">
                        <div className="empty-state-icon">
                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <line x1="16" y1="13" x2="8" y2="13"></line>
                                <line x1="16" y1="17" x2="8" y2="17"></line>
                                <polyline points="10 9 9 9 8 9"></polyline>
                            </svg>
                        </div>
                        <h2>No Report Generated Yet</h2>
                        <p>Click "Generate Report" to analyze your customer feedback data and get AI-powered insights.</p>
                    </div>
                )}

                {!loading && chartsData && (
                    <div className="charts-wrapper">
                        <h2 className="section-title">Data Visualizations</h2>
                        <ChartSection chartsData={chartsData} />
                    </div>
                )}

                {!loading && reportData && (
                    <ReportDisplay report={reportData.report} insights={reportData.insights} />
                )}
            </main>
        </div>
    );
};

export default AdminPanel;
