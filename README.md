# CRM RAG Analytics System

A comprehensive Customer Relationship Management (CRM) analytics application that uses Retrieval-Augmented Generation (RAG) with Groq LLM to analyze customer feedback data and generate intelligent reports with visualizations.

## Features

- 🤖 **AI-Powered Analysis**: Uses Groq's LLM (llama-3.3-70b-versatile) for intelligent report generation
- 📊 **Interactive Visualizations**: Beautiful charts with Recharts (pie, bar, line charts)
- 📄 **PDF Export**: Generate professional PDF reports with embedded charts
- 🎨 **Modern UI**: Glassmorphism design with gradients and smooth animations
- 🔄 **Database Ready**: Prepared for MySQL integration (currently using CSV)
- ⚡ **Fast API**: Built with Python FastAPI for high performance

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **Groq** - LLM API for RAG
- **Pandas** - Data analysis
- **ReportLab** - PDF generation
- **Matplotlib** - Chart generation
- **MySQL Connector** - Database support (prepared for future use)

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Recharts** - Data visualization
- **Axios** - API client

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Groq API key (get one from [Groq Console](https://console.groq.com))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Groq API key to the `.env` file:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

4. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start the Backend**: Run `python main.py` in the `backend` directory
2. **Start the Frontend**: Run `npm run dev` in the `frontend` directory
3. **Open the App**: Navigate to `http://localhost:3000`
4. **Generate Report**: Click "Generate Report" to analyze the data
5. **Download PDF**: Click "Download PDF" to export the report

## API Endpoints

- `GET /` - API information
- `POST /api/analyze-data` - Load and analyze CSV data
- `GET /api/charts-data` - Get formatted data for charts
- `POST /api/generate-report` - Generate AI-powered report
- `POST /api/generate-pdf` - Generate PDF report
- `GET /api/download-pdf/{filename}` - Download generated PDF
- `GET /api/health` - Health check endpoint
- `GET /api/database/test` - Test MySQL connection

## Data Source

Currently using CSV file (`data/Datafinal1.csv`) with customer feedback data containing:
- Complaint text
- Category (Technical Issues, Delivery, Billing, Product Quality, Customer Service, etc.)
- Sentiment (Best, Good, Average, Fair, Bad)
- Rating (1-5)
- Confidence score
- Timestamp

## Future Database Migration

The application is prepared for MySQL database integration:

1. Update `.env` file with your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=crm_database
DB_USER=root
DB_PASSWORD=your_password
USE_DATABASE=true
DATA_SOURCE=database
```

2. Create the database table (run once):
```python
from db_config import DatabaseConfig
db = DatabaseConfig()
db.create_sample_table()
```

3. The application will automatically switch to database mode when `USE_DATABASE=true`

## Project Structure

```
crm-rag-system/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_engine.py        # RAG implementation with Groq
│   ├── data_processor.py    # Data analysis utilities
│   ├── pdf_generator.py     # PDF generation with charts
│   ├── db_config.py         # MySQL database configuration
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── data/
│       └── Datafinal1.csv   # Sample data
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── AdminPanel.jsx        # Main dashboard
    │   │   ├── ChartSection.jsx      # Visualizations
    │   │   └── ReportDisplay.jsx     # Report renderer
    │   ├── services/
    │   │   └── api.js                # API client
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css                 # Global styles
    ├── package.json
    ├── vite.config.js
    └── index.html
```

## Customization

### Adding New Chart Types
Edit `frontend/src/components/ChartSection.jsx` and add new Recharts components.

### Modifying Report Template
Edit the prompt in `backend/rag_engine.py` in the `_create_report_prompt` method.

### Changing LLM Model
Update the `model` variable in `backend/rag_engine.py` (options: llama-3.3-70b-versatile, mixtral-8x7b-32768, etc.)

## Troubleshooting

**Backend won't start:**
- Ensure you have set `GROQ_API_KEY` in `.env`
- Check Python version (3.8+)
- Verify all dependencies are installed

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Charts not displaying:**
- Ensure data is loaded correctly
- Check browser console for errors

## License

MIT License - Feel free to use this project for your own purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
