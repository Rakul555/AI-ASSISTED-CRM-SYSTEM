from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
from datetime import datetime
from typing import Dict, Any, List
import base64
import re

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _convert_markdown_bold(self, text: str) -> str:
        """Convert markdown bold (**text**) to HTML bold (<b>text</b>)"""
        # Use regex to replace **text** with <b>text</b>
        return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    def generate_pdf(self, report_text: str, analytics: Dict[str, Any], filename: str = None) -> str:
        """Generate PDF report with charts"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'crm_report_{timestamp}.pdf'
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        story = []
        
        # Add title
        title = Paragraph("CRM Analytics Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add generation date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, self.styles['CustomBody'])
        story.append(date_para)
        story.append(Spacer(1, 30))
        
        # Add report content
        self._add_report_content(story, report_text)
        
        # Add page break before charts
        story.append(PageBreak())
        
        # Add charts
        story.append(Paragraph("Data Visualizations", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        self._add_charts(story, analytics)
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def _add_report_content(self, story: List, report_text: str):
        """Add formatted report content to PDF"""
        # Split report into lines and process
        lines = report_text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Check for markdown headings (## Heading)
            if line.startswith('##'):
                heading_text = line.replace('##', '').strip()
                heading = Paragraph(heading_text, self.styles['CustomHeading'])
                story.append(heading)
                i += 1
                continue
            
            # Check for main heading (# Heading)
            if line.startswith('#'):
                heading_text = line.replace('#', '').strip()
                heading = Paragraph(heading_text, self.styles['CustomTitle'])
                story.append(heading)
                story.append(Spacer(1, 12))
                i += 1
                continue
            
            # Check for bullet points
            if line.startswith('-') or line.startswith('*'):
                # Collect consecutive bullet points
                bullet_lines = []
                while i < len(lines) and (lines[i].strip().startswith('-') or lines[i].strip().startswith('*')):
                    bullet_text = lines[i].strip()[1:].strip()
                    # Handle bold text (**text**) properly
                    bullet_text = self._convert_markdown_bold(bullet_text)
                    bullet_lines.append(bullet_text)
                    i += 1
                
                # Add bullets as paragraphs with bullet style
                for bullet in bullet_lines:
                    para = Paragraph(f'• {bullet}', self.styles['CustomBody'])
                    story.append(para)
                story.append(Spacer(1, 8))
                continue
            
            # Check for numbered lists
            if line and len(line) > 2 and line[0].isdigit() and line[1] == '.':
                # Collect consecutive numbered items
                numbered_lines = []
                while i < len(lines) and len(lines[i].strip()) > 2 and lines[i].strip()[0].isdigit() and lines[i].strip()[1] == '.':
                    item_text = lines[i].strip().split('.', 1)[1].strip()
                    # Handle bold text properly
                    item_text = self._convert_markdown_bold(item_text)
                    numbered_lines.append(item_text)
                    i += 1
                
                # Add numbered items
                for idx, item in enumerate(numbered_lines, 1):
                    para = Paragraph(f'{idx}. {item}', self.styles['CustomBody'])
                    story.append(para)
                story.append(Spacer(1, 8))
                continue
            
            # Regular paragraph
            # Handle bold text in paragraphs properly
            paragraph_text = self._convert_markdown_bold(line)
            para = Paragraph(paragraph_text, self.styles['CustomBody'])
            story.append(para)
            story.append(Spacer(1, 6))
            i += 1
    
    def _add_charts(self, story: List, analytics: Dict[str, Any]):
        """Generate and add charts to PDF"""
        # Sentiment Distribution Pie Chart
        sentiment_chart = self._create_sentiment_pie_chart(analytics['sentiment_distribution'])
        if sentiment_chart:
            story.append(Paragraph("Sentiment Distribution", self.styles['CustomHeading']))
            story.append(sentiment_chart)
            story.append(Spacer(1, 20))
        
        # Category Distribution Bar Chart
        category_chart = self._create_category_bar_chart(analytics['category_distribution'])
        if category_chart:
            story.append(Paragraph("Complaints by Category", self.styles['CustomHeading']))
            story.append(category_chart)
            story.append(Spacer(1, 20))
        
        # Rating by Category Bar Chart
        rating_chart = self._create_rating_bar_chart(analytics['rating_by_category'])
        if rating_chart:
            story.append(PageBreak())
            story.append(Paragraph("Average Rating by Category", self.styles['CustomHeading']))
            story.append(rating_chart)
            story.append(Spacer(1, 20))
    
    def _create_sentiment_pie_chart(self, sentiment_data: Dict[str, int]) -> Image:
        """Create sentiment distribution pie chart"""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            labels = list(sentiment_data.keys())
            sizes = list(sentiment_data.values())
            colors_map = {
                'Best': '#4caf50',
                'Good': '#8bc34a',
                'Average': '#ffc107',
                'Fair': '#ff9800',
                'Bad': '#f44336'
            }
            colors_list = [colors_map.get(label, '#9e9e9e') for label in labels]
            
            ax.pie(sizes, labels=labels, colors=colors_list, autopct='%1.1f%%',
                   startangle=90, textprops={'fontsize': 10})
            ax.axis('equal')
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Create ReportLab Image
            img = Image(img_buffer, width=5*inch, height=3.75*inch)
            return img
            
        except Exception as e:
            print(f"Error creating sentiment chart: {e}")
            return None
    
    def _create_category_bar_chart(self, category_data: Dict[str, int]) -> Image:
        """Create category distribution bar chart"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            categories = list(category_data.keys())
            counts = list(category_data.values())
            
            bars = ax.barh(categories, counts, color='#3f51b5')
            ax.set_xlabel('Number of Complaints', fontsize=11)
            ax.set_title('Complaints Distribution by Category', fontsize=13, fontweight='bold')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{int(width)}', ha='left', va='center', fontsize=9)
            
            plt.tight_layout()
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Create ReportLab Image
            img = Image(img_buffer, width=6*inch, height=3.6*inch)
            return img
            
        except Exception as e:
            print(f"Error creating category chart: {e}")
            return None
    
    def _create_rating_bar_chart(self, rating_data: Dict[str, float]) -> Image:
        """Create rating by category bar chart"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            categories = list(rating_data.keys())
            ratings = list(rating_data.values())
            
            # Color bars based on rating
            colors_list = ['#4caf50' if r >= 4 else '#ffc107' if r >= 3 else '#f44336' for r in ratings]
            
            bars = ax.barh(categories, ratings, color=colors_list)
            ax.set_xlabel('Average Rating', fontsize=11)
            ax.set_xlim(0, 5)
            ax.set_title('Average Rating by Category', fontsize=13, fontweight='bold')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{width:.2f}', ha='left', va='center', fontsize=9)
            
            plt.tight_layout()
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Create ReportLab Image
            img = Image(img_buffer, width=6*inch, height=3.6*inch)
            return img
            
        except Exception as e:
            print(f"Error creating rating chart: {e}")
            return None
