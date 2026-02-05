import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import os

class DataProcessor:
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or os.path.join(os.path.dirname(__file__), 'data', 'Datafinal1.csv')
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """Load CSV data into pandas DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_path)
            return self.df
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get distribution of sentiments"""
        if self.df is None:
            self.load_data()
        
        sentiment_counts = self.df['sentiment'].value_counts().to_dict()
        return sentiment_counts
    
    def get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of complaint categories"""
        if self.df is None:
            self.load_data()
        
        category_counts = self.df['category'].value_counts().to_dict()
        return category_counts
    
    def get_rating_by_category(self) -> Dict[str, float]:
        """Get average rating per category"""
        if self.df is None:
            self.load_data()
        
        rating_by_category = self.df.groupby('category')['rating'].mean().to_dict()
        return {k: round(v, 2) for k, v in rating_by_category.items()}
    
    def get_priority_issues(self, rating_threshold: int = 2) -> List[Dict[str, Any]]:
        """Get high-priority issues (low ratings)"""
        if self.df is None:
            self.load_data()
        
        priority_df = self.df[self.df['rating'] <= rating_threshold]
        return priority_df[['id', 'complaint_text', 'category', 'sentiment', 'rating']].to_dict('records')
    
    def get_time_series_data(self) -> List[Dict[str, Any]]:
        """Get complaints over time"""
        if self.df is None:
            self.load_data()
        
        # Convert created_at to datetime
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        
        # Group by date
        time_series = self.df.groupby(self.df['created_at'].dt.date).size().reset_index()
        time_series.columns = ['date', 'count']
        time_series['date'] = time_series['date'].astype(str)
        
        return time_series.to_dict('records')
    
    def get_confidence_stats(self) -> Dict[str, float]:
        """Get confidence score statistics"""
        if self.df is None:
            self.load_data()
        
        return {
            'mean': round(self.df['confidence'].mean(), 3),
            'median': round(self.df['confidence'].median(), 3),
            'min': round(self.df['confidence'].min(), 3),
            'max': round(self.df['confidence'].max(), 3)
        }
    
    def get_category_sentiment_correlation(self) -> List[Dict[str, Any]]:
        """Get sentiment distribution per category"""
        if self.df is None:
            self.load_data()
        
        correlation = self.df.groupby(['category', 'sentiment']).size().reset_index(name='count')
        return correlation.to_dict('records')
    
    def get_all_analytics(self) -> Dict[str, Any]:
        """Get all analytics data"""
        return {
            'sentiment_distribution': self.get_sentiment_distribution(),
            'category_distribution': self.get_category_distribution(),
            'rating_by_category': self.get_rating_by_category(),
            'priority_issues': self.get_priority_issues(),
            'time_series': self.get_time_series_data(),
            'confidence_stats': self.get_confidence_stats(),
            'category_sentiment_correlation': self.get_category_sentiment_correlation(),
            'total_complaints': len(self.df) if self.df is not None else 0
        }
    
    def get_data_summary(self) -> str:
        """Get a text summary of the data for RAG context"""
        if self.df is None:
            self.load_data()
        
        analytics = self.get_all_analytics()
        
        summary = f"""
Customer Feedback Data Summary:
- Total Complaints: {analytics['total_complaints']}

Sentiment Distribution:
{self._format_dict(analytics['sentiment_distribution'])}

Category Distribution:
{self._format_dict(analytics['category_distribution'])}

Average Rating by Category:
{self._format_dict(analytics['rating_by_category'])}

Confidence Score Statistics:
{self._format_dict(analytics['confidence_stats'])}

Priority Issues Count (Rating ≤ 2): {len(analytics['priority_issues'])}

Top Priority Issues:
{self._format_priority_issues(analytics['priority_issues'][:5])}
"""
        return summary
    
    def _format_dict(self, data: Dict) -> str:
        """Format dictionary for readable output"""
        return "\n".join([f"  - {k}: {v}" for k, v in data.items()])
    
    def _format_priority_issues(self, issues: List[Dict]) -> str:
        """Format priority issues for readable output"""
        formatted = []
        for issue in issues:
            formatted.append(f"  • [{issue['category']}] Rating: {issue['rating']} - {issue['complaint_text'][:100]}...")
        return "\n".join(formatted)
