from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from datetime import datetime

from data_processor import DataProcessor
from rag_engine import RAGEngine
from pdf_generator import PDFGenerator
from db_config import DatabaseConfig

app = FastAPI(title="CRM RAG Analytics API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_processor = DataProcessor()
rag_engine = RAGEngine()
pdf_generator = PDFGenerator()
db_config = DatabaseConfig()

# Response models
class AnalyticsResponse(BaseModel):
    status: str
    data: Dict[str, Any]

class ReportResponse(BaseModel):
    status: str
    report: str
    insights: List[str]
    analytics: Dict[str, Any]

class PDFResponse(BaseModel):
    status: str
    filename: str
    download_url: str

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "CRM RAG Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "analytics": "/api/analyze-data",
            "report": "/api/generate-report",
            "charts": "/api/charts-data",
            "pdf": "/api/generate-pdf"
        }
    }

@app.post("/api/analyze-data", response_model=AnalyticsResponse)
async def analyze_data():
    """Load and analyze CSV data"""
    try:
        analytics = data_processor.get_all_analytics()
        
        return AnalyticsResponse(
            status="success",
            data=analytics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")

@app.get("/api/charts-data")
async def get_charts_data():
    """Get data formatted for charts"""
    try:
        analytics = data_processor.get_all_analytics()
        
        # Format data for frontend charts
        charts_data = {
            "sentiment_distribution": [
                {"name": k, "value": v} 
                for k, v in analytics['sentiment_distribution'].items()
            ],
            "category_distribution": [
                {"name": k, "value": v} 
                for k, v in analytics['category_distribution'].items()
            ],
            "rating_by_category": [
                {"category": k, "rating": v} 
                for k, v in analytics['rating_by_category'].items()
            ],
            "time_series": analytics['time_series'],
            "total_complaints": analytics['total_complaints'],
            "priority_count": len(analytics['priority_issues']),
            "confidence_stats": analytics['confidence_stats']
        }
        
        return {
            "status": "success",
            "data": charts_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting charts data: {str(e)}")

@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report():
    """Generate comprehensive report using RAG"""
    try:
        # Get analytics data
        analytics = data_processor.get_all_analytics()
        data_summary = data_processor.get_data_summary()
        
        # Generate report using RAG
        report = rag_engine.generate_report(data_summary, analytics)
        
        # Generate quick insights
        insights = rag_engine.generate_quick_insights(analytics)
        
        return ReportResponse(
            status="success",
            report=report,
            insights=insights,
            analytics=analytics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.post("/api/generate-pdf")
async def generate_pdf():
    """Generate PDF report with charts"""
    try:
        # Get analytics and report
        analytics = data_processor.get_all_analytics()
        data_summary = data_processor.get_data_summary()
        report = rag_engine.generate_report(data_summary, analytics)
        
        # Generate PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'crm_report_{timestamp}.pdf'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        pdf_generator.generate_pdf(report, analytics, filepath)
        
        return {
            "status": "success",
            "filename": filename,
            "message": "PDF generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.get("/api/download-pdf/{filename}")
async def download_pdf(filename: str):
    """Download generated PDF file"""
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        return FileResponse(
            filepath,
            media_type='application/pdf',
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading PDF: {str(e)}")

@app.get("/api/database/test")
async def test_database_connection():
    """Test MySQL database connection"""
    try:
        is_connected = db_config.test_connection()
        return {
            "status": "success" if is_connected else "failed",
            "connected": is_connected,
            "message": "Database connection successful" if is_connected else "Could not connect to database"
        }
    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "message": str(e)
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_source": "CSV" if not db_config.use_database else "MySQL"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
