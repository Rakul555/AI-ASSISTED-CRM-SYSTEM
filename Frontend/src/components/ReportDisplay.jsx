import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ReportDisplay.css';

const ReportDisplay = ({ report, insights }) => {
    if (!report) {
        return null;
    }

    return (
        <div className="report-display">
            {insights && insights.length > 0 && (
                <div className="insights-section">
                    <h3 className="insights-title">Quick Insights</h3>
                    <div className="insights-grid">
                        {insights.map((insight, index) => (
                            <div key={index} className="insight-card glass">
                                <p>{insight}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className="report-content card">
                <div className="report-header">
                    <h2>AI-Generated Analysis Report</h2>
                </div>
                <div className="report-body">
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                            h1: ({ node, ...props }) => <h1 className="markdown-h1" {...props} />,
                            h2: ({ node, ...props }) => <h2 className="markdown-h2" {...props} />,
                            h3: ({ node, ...props }) => <h3 className="markdown-h3" {...props} />,
                            p: ({ node, ...props }) => <p className="markdown-p" {...props} />,
                            ul: ({ node, ...props }) => <ul className="markdown-ul" {...props} />,
                            ol: ({ node, ...props }) => <ol className="markdown-ol" {...props} />,
                            li: ({ node, ...props }) => <li className="markdown-li" {...props} />,
                            strong: ({ node, ...props }) => <strong className="markdown-strong" {...props} />,
                        }}
                    >
                        {report}
                    </ReactMarkdown>
                </div>
            </div>
        </div>
    );
};

export default ReportDisplay;
