import React from 'react';
import {
    PieChart, Pie, BarChart, Bar, LineChart, Line,
    XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer, Cell
} from 'recharts';
import './ChartSection.css';

const COLORS = {
    Best: '#4caf50',
    Good: '#8bc34a',
    Average: '#ffc107',
    Fair: '#ff9800',
    Bad: '#f44336'
};

const CATEGORY_COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#43e97b', '#38f9d7', '#4facfe', '#00f2fe'];

const ChartSection = ({ chartsData }) => {
    if (!chartsData) {
        return (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p style={{ color: 'var(--text-muted)' }}>No data available for charts</p>
            </div>
        );
    }

    const { sentiment_distribution, category_distribution, rating_by_category, time_series } = chartsData;

    return (
        <div className="charts-container">
            <div className="charts-grid">
                {/* Sentiment Distribution Pie Chart */}
                <div className="chart-card card fade-in">
                    <div className="card-header">
                        <h3 className="card-title">Sentiment Distribution</h3>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={sentiment_distribution}
                                dataKey="value"
                                nameKey="name"
                                cx="50%"
                                cy="50%"
                                outerRadius={100}
                                label={(entry) => `${entry.name}: ${entry.value}`}
                                labelLine={false}
                            >
                                {sentiment_distribution?.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#9e9e9e'} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-card)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: 'var(--radius-sm)'
                                }}
                            />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Category Distribution Bar Chart */}
                <div className="chart-card card fade-in" style={{ animationDelay: '0.1s' }}>
                    <div className="card-header">
                        <h3 className="card-title">Complaints by Category</h3>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={category_distribution}>
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                            <XAxis
                                dataKey="name"
                                stroke="var(--text-secondary)"
                                tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
                                angle={-45}
                                textAnchor="end"
                                height={100}
                            />
                            <YAxis stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-card)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: 'var(--radius-sm)'
                                }}
                            />
                            <Bar dataKey="value" name="Count">
                                {category_distribution?.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Rating by Category Bar Chart */}
                <div className="chart-card card fade-in" style={{ animationDelay: '0.2s' }}>
                    <div className="card-header">
                        <h3 className="card-title">Average Rating by Category</h3>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={rating_by_category} layout="horizontal">
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                            <XAxis
                                type="number"
                                domain={[0, 5]}
                                stroke="var(--text-secondary)"
                                tick={{ fill: 'var(--text-secondary)' }}
                            />
                            <YAxis
                                type="category"
                                dataKey="category"
                                stroke="var(--text-secondary)"
                                tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
                                width={150}
                            />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-card)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: 'var(--radius-sm)'
                                }}
                            />
                            <Bar dataKey="rating" name="Avg Rating">
                                {rating_by_category?.map((entry, index) => {
                                    const color = entry.rating >= 4 ? '#4caf50' : entry.rating >= 3 ? '#ffc107' : '#f44336';
                                    return <Cell key={`cell-${index}`} fill={color} />;
                                })}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Time Series Line Chart */}
                <div className="chart-card card fade-in" style={{ animationDelay: '0.3s' }}>
                    <div className="card-header">
                        <h3 className="card-title">Complaints Timeline</h3>
                    </div>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={time_series}>
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                            <XAxis
                                dataKey="date"
                                stroke="var(--text-secondary)"
                                tick={{ fill: 'var(--text-secondary)', fontSize: 10 }}
                                angle={-45}
                                textAnchor="end"
                                height={80}
                            />
                            <YAxis stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-card)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: 'var(--radius-sm)'
                                }}
                            />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="count"
                                stroke="#667eea"
                                strokeWidth={3}
                                dot={{ fill: '#667eea', r: 5 }}
                                activeDot={{ r: 8 }}
                                name="Complaints"
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default ChartSection;
