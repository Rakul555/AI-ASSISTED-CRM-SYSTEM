# Setup Instructions

## Quick Start

### 1. Backend Setup

Open a terminal and navigate to the backend directory:

```bash
cd crm-rag-system/backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

**IMPORTANT**: Edit the `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

Start the server:
```bash
python main.py
```

Server will run at: `http://localhost:8000`

### 2. Frontend Setup

Open a **new terminal** and navigate to the frontend directory:

```bash
cd crm-rag-system/frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

Frontend will run at: `http://localhost:3000`

### 3. Access the Application

Open your browser and go to: `http://localhost:3000`

Click "Generate Report" to analyze the customer feedback data!

## Get Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key and paste it in `backend/.env`

## Troubleshooting

If you get an error about missing packages:
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

If the backend says "GROQ_API_KEY not found":
- Make sure you edited `backend/.env` file
- Replace `your_groq_api_key_here` with your actual key
