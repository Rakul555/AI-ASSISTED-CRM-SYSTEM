import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
    // Get analytics data
    getAnalytics: async () => {
        const response = await axios.post(`${API_BASE_URL}/analyze-data`);
        return response.data;
    },

    // Get charts data
    getChartsData: async () => {
        const response = await axios.get(`${API_BASE_URL}/charts-data`);
        return response.data;
    },

    // Generate report
    generateReport: async () => {
        const response = await axios.post(`${API_BASE_URL}/generate-report`);
        return response.data;
    },

    // Generate PDF
    generatePDF: async () => {
        const response = await axios.post(`${API_BASE_URL}/generate-pdf`);
        return response.data;
    },

    // Download PDF
    downloadPDF: (filename) => {
        window.open(`${API_BASE_URL}/download-pdf/${filename}`, '_blank');
    },

    // Health check
    healthCheck: async () => {
        const response = await axios.get(`${API_BASE_URL}/health`);
        return response.data;
    }
};
