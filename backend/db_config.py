import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration for future MySQL integration"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.database = os.getenv('DB_NAME', 'crm_database')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.use_database = os.getenv('USE_DATABASE', 'false').lower() == 'true'
        
    def get_connection(self):
        """Establish MySQL connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            if connection.is_connected():
                return connection
        except Error as e:
            raise Exception(f"Error connecting to MySQL: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            connection = self.get_connection()
            if connection.is_connected():
                connection.close()
                return True
            return False
        except Exception:
            return False
    
    def fetch_complaints_data(self):
        """Fetch complaints data from MySQL database (for future use)"""
        if not self.use_database:
            raise Exception("Database mode is not enabled. Set USE_DATABASE=true in .env")
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Example query - adjust based on your actual table structure
            query = """
                SELECT id, complaint_text, category, sentiment, rating, confidence, created_at
                FROM complaints
                ORDER BY created_at DESC
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return results
            
        except Error as e:
            raise Exception(f"Error fetching data from MySQL: {str(e)}")
    
    def create_sample_table(self):
        """Create sample complaints table structure (run this once to setup)"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            create_table_query = """
                CREATE TABLE IF NOT EXISTS complaints (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    complaint_text TEXT NOT NULL,
                    category VARCHAR(100),
                    sentiment VARCHAR(50),
                    rating INT,
                    confidence DECIMAL(5,3),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            cursor.execute(create_table_query)
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return {"message": "Table created successfully"}
            
        except Error as e:
            raise Exception(f"Error creating table: {str(e)}")
