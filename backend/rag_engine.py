from groq import Groq
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'your_groq_api_key_here':
            raise ValueError("Please set GROQ_API_KEY in .env file")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Using the latest Llama model
        
    def create_chunks(self, data: str, chunk_size: int = 2000) -> List[str]:
        """Split data into chunks for context"""
        words = data.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_size += len(word) + 1
            if current_size > chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def generate_report(self, data_summary: str, analytics: Dict[str, Any]) -> str:
        """Generate comprehensive report using RAG with Groq"""
        
        # Create context from data
        context = self._build_context(data_summary, analytics)
        
        # Create prompt for report generation
        prompt = self._create_report_prompt(context)
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert data analyst specializing in customer feedback analysis and CRM insights. Generate comprehensive, actionable reports with clear insights and recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=3000
            )
            
            report = chat_completion.choices[0].message.content
            return report
            
        except Exception as e:
            raise Exception(f"Error generating report with Groq: {str(e)}")
    
    def _build_context(self, data_summary: str, analytics: Dict[str, Any]) -> str:
        """Build context from data and analytics"""
        context = f"""
{data_summary}

Detailed Analytics:

Sentiment Breakdown:
{self._format_sentiment_data(analytics['sentiment_distribution'])}

Category Analysis:
{self._format_category_data(analytics['category_distribution'], analytics['rating_by_category'])}

Time Series Data:
Latest complaints show activity from {analytics['time_series'][0]['date']} to {analytics['time_series'][-1]['date']}

Priority Issues:
{len(analytics['priority_issues'])} complaints require immediate attention (ratings 1-2)

Category-Sentiment Correlation:
{self._format_correlation_data(analytics['category_sentiment_correlation'])}
"""
        return context
    
    def _create_report_prompt(self, context: str) -> str:
        """Create prompt for report generation"""
        prompt = f"""
Based on the following customer feedback data and analytics, generate a comprehensive CRM Analysis Report.

DATA AND ANALYTICS:
{context}

IMPORTANT FORMATTING INSTRUCTIONS:
- Use proper markdown formatting throughout the report
- Use clear section headers with ## for main sections
- Use bullet points (- or *) for lists
- Use **bold** for emphasis on key metrics and important findings
- Use numbered lists for recommendations and action items
- Keep paragraphs concise and well-structured
- Include specific numbers and percentages in your analysis

Please generate a detailed report with the following structure:

## Executive Summary
Provide a brief overview (2-3 paragraphs) covering:
- Total complaints analyzed
- Overall sentiment trend
- Most critical findings
- Key recommendation

## Sentiment Analysis
Analyze the sentiment distribution:
- Break down each sentiment category (Best, Good, Average, Fair, Bad) with percentages
- Identify the dominant sentiment
- Compare positive vs negative feedback ratios
- Highlight any concerning trends

## Category Breakdown
Detailed analysis of complaint categories:
- List all categories with complaint counts
- Identify the top 3 most problematic categories
- Provide specific insights for each major category
- Include average ratings per category

## Priority Issues
Focus on high-priority problems:
- List the number of critical complaints (rating 1-2)
- Identify which categories have the most urgent issues
- Provide 3-5 specific examples of critical complaints
- Highlight patterns in priority issues

## Trends and Patterns
Analyze temporal and categorical patterns:
- Discuss time-based trends in complaint volume
- Identify correlations between categories and sentiments
- Point out emerging issues or recurring themes
- Note any unusual patterns in the data

## Key Recommendations
Provide 5-7 actionable recommendations:
1. Immediate actions for priority issues
2. Short-term improvements for problematic categories
3. Long-term strategies for customer satisfaction
4. Specific process improvements
5. Team training or resource allocation needs

## Conclusion
Summarize in 2-3 paragraphs:
- Overall assessment of customer feedback health
- Most critical action items
- Expected impact of recommended changes
- Next steps for the CRM team

Use clear, professional language and ensure all sections are well-formatted with proper markdown syntax.
"""
        return prompt
    
    def _format_sentiment_data(self, sentiment_dist: Dict[str, int]) -> str:
        """Format sentiment distribution"""
        total = sum(sentiment_dist.values())
        formatted = []
        for sentiment, count in sentiment_dist.items():
            percentage = (count / total * 100) if total > 0 else 0
            formatted.append(f"  - {sentiment}: {count} ({percentage:.1f}%)")
        return "\n".join(formatted)
    
    def _format_category_data(self, category_dist: Dict[str, int], rating_by_cat: Dict[str, float]) -> str:
        """Format category distribution with ratings"""
        formatted = []
        for category, count in category_dist.items():
            avg_rating = rating_by_cat.get(category, 0)
            formatted.append(f"  - {category}: {count} complaints (Avg Rating: {avg_rating})")
        return "\n".join(formatted)
    
    def _format_correlation_data(self, correlation: List[Dict[str, Any]]) -> str:
        """Format category-sentiment correlation"""
        formatted = []
        current_category = None
        
        for item in sorted(correlation, key=lambda x: x['category']):
            if item['category'] != current_category:
                current_category = item['category']
                formatted.append(f"\n  {current_category}:")
            formatted.append(f"    - {item['sentiment']}: {item['count']}")
        
        return "\n".join(formatted)
    
    def generate_quick_insights(self, analytics: Dict[str, Any]) -> List[str]:
        """Generate quick insights from analytics"""
        insights = []
        
        # Sentiment insight
        sentiment_dist = analytics['sentiment_distribution']
        total_complaints = analytics['total_complaints']
        bad_complaints = sentiment_dist.get('Bad', 0)
        if bad_complaints / total_complaints > 0.3:
            insights.append(f"⚠️ High volume of negative feedback: {bad_complaints} complaints ({bad_complaints/total_complaints*100:.1f}%)")
        
        # Priority insight
        priority_count = len(analytics['priority_issues'])
        if priority_count > total_complaints * 0.2:
            insights.append(f"🔴 {priority_count} high-priority issues need immediate attention")
        
        # Category insight
        category_dist = analytics['category_distribution']
        top_category = max(category_dist.items(), key=lambda x: x[1])
        insights.append(f"📊 Most complaints in: {top_category[0]} ({top_category[1]} complaints)")
        
        # Rating insight
        rating_by_cat = analytics['rating_by_category']
        worst_category = min(rating_by_cat.items(), key=lambda x: x[1])
        insights.append(f"⭐ Lowest rated category: {worst_category[0]} (Avg: {worst_category[1]}/5)")
        
        return insights
