"""
Napa Valley Wine Business Conversational Concierge Chatbot
Full production version with real AI responses
Chatbot Identity: Tohin - Personal Wine Concierge
"""

import os
import json
import requests
from typing import List
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NapaValleyConciergeChatbot:
    """Main chatbot class that handles conversation and query routing."""

    def __init__(self):
        """Initialize the chatbot with all necessary services."""
        load_dotenv()

        # Initialize API keys
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required!")

        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

        # Initialize ChromaDB
        self.setup_chromadb()

        # Configuration
        self.temperature = 0.7
        self.max_tokens = 1000

        logger.info("Tohin - Napa Valley Concierge Chatbot initialized successfully!")

    def setup_chromadb(self):
        """Set up ChromaDB connection and collection."""
        try:
            chroma_db_path = './chroma_db'
            self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)

            # Get the knowledge collection
            self.knowledge_collection = self.chroma_client.get_collection("wine_business_knowledge")
            logger.info("Connected to ChromaDB knowledge base")

        except Exception as e:
            logger.error(f"Error connecting to ChromaDB: {e}")
            self.knowledge_collection = None

    def classify_query_intent(self, query: str) -> str:
        """Classify the user's query to determine the appropriate response strategy."""
        query_lower = query.lower()

        # Business-related keywords
        business_keywords = [
            'wine', 'tasting', 'vineyard', 'winery', 'hours', 'reservation',
            'price', 'cost', 'shipping', 'club', 'tour', 'location', 'address',
            'cabernet', 'chardonnay', 'pinot', 'merlot', 'bottle', 'vintage',
            'cellar', 'harvest', 'barrels', 'sommelier', 'pairing', 'taste',
            'flavor', 'aroma', 'notes'
        ]

        # Weather keywords
        weather_keywords = [
            'weather', 'temperature', 'rain', 'sunny', 'forecast', 'climate',
            'hot', 'cold', 'warm', 'degrees', 'fahrenheit', 'celsius'
        ]

        # News/real-time keywords
        news_keywords = [
            'news', 'latest', 'recent', 'current', 'today', 'happening',
            'events', 'festival', 'what\'s new', 'updates'
        ]

        # Check for business queries first
        if any(keyword in query_lower for keyword in business_keywords):
            return 'business'

        # Check for weather queries
        if any(keyword in query_lower for keyword in weather_keywords):
            return 'weather'

        # Check for news queries
        if any(keyword in query_lower for keyword in news_keywords):
            return 'news'

        # Everything else is chitchat
        return 'chitchat'

    def search_knowledge_base(self, query: str, n_results: int = 3) -> List[str]:
        """Search the ChromaDB knowledge base for relevant information."""
        if not self.knowledge_collection:
            logger.error("Knowledge collection not available")
            return []

        try:
            # Generate embedding for the query
            query_embedding = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )

            # Search similar documents
            results = self.knowledge_collection.query(
                query_embeddings=[query_embedding['embedding']],
                n_results=n_results
            )

            # Extract relevant documents
            relevant_docs = results['documents'][0] if results['documents'] else []
            logger.info(f"Found {len(relevant_docs)} relevant documents")

            return relevant_docs

        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []

    def get_realtime_info(self, query: str) -> str:
        """Get real-time information using Perplexity API."""
        if not self.perplexity_api_key:
            return "Real-time information service is currently unavailable."

        try:
            url = "https://api.perplexity.ai/chat/completions"

            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are helping Tohin, a helpful assistant, provide current information about Napa Valley, wine industry, and related topics."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            return data['choices'][0]['message']['content']

        except Exception as e:
            logger.error(f"Error fetching real-time information: {e}")
            return "I'm sorry, I couldn't retrieve the latest information at this time."

    def get_weather_info(self, location: str = "Napa, CA") -> str:
        """Get current weather information for specified location."""
        # Try both possible environment variable names for the API key
        api_key = os.getenv('WEATHER_API_KEY') or os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            return "Weather service is currently unavailable."

        try:
            # Use HTTPS URL for OpenWeatherMap API
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': api_key,
                'units': 'imperial'  # Fahrenheit units
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Format the weather information for user-friendly output
            weather_info = f"""
Current weather in {data['name']}:
• Temperature: {data['main']['temp']}°F (feels like {data['main']['feels_like']}°F)
• Condition: {data['weather'][0]['description'].title()}
• Humidity: {data['main']['humidity']}%
• Wind Speed: {data['wind'].get('speed', 'N/A')} mph
"""
            return weather_info.strip()

        except requests.exceptions.HTTPError as e:
            # Specific handling for HTTP errors
            if response.status_code == 401:
                return "The weather API key is invalid or not activated yet. Please check your API key."
            elif response.status_code == 404:
                return "I couldn't find weather information for the specified location."
            else:
                return f"Sorry, I couldn't fetch the weather information. Error: {e}"
        except Exception as e:
            # General exception catcher
            return f"Sorry, I couldn't fetch the weather information due to an unexpected error: {e}"

    def generate_response(self, query: str, context: str, intent: str) -> str:
        """Generate a response using Gemini with appropriate context."""

        # Create system prompt based on intent
        if intent == 'business':
            system_prompt = """You are Tohin, a friendly and knowledgeable personal concierge for Napa Valley Premium Wines. 
            Use the provided business information to answer questions about our winery, wines, tastings, 
            tours, and services. Be warm, professional, and helpful. Always introduce yourself as Tohin when 
            meeting someone new or when asked about yourself."""

        elif intent == 'weather':
            system_prompt = """You are Tohin, a helpful personal concierge providing weather information for visitors 
            to Napa Valley. If weather data is unavailable, provide general seasonal advice for Napa Valley 
            and suggest indoor/outdoor activities. Always identify yourself as Tohin when asked."""

        elif intent == 'news':
            system_prompt = """You are Tohin, a knowledgeable personal concierge sharing information about 
            Napa Valley, wine industry, and local events. Present information in an engaging way. 
            Always introduce yourself as Tohin when appropriate."""

        elif intent == 'chitchat':
            system_prompt = """You are Tohin, a friendly and personable concierge at Napa Valley Premium Wines. 
            You love casual conversation and are great at small talk. When someone asks about yourself, 
            introduce yourself as Tohin - a personal wine concierge who helps visitors discover the best 
            of Napa Valley. Keep responses warm, engaging, and conversational. Answer questions naturally 
            and try to steer conversation toward wine, the winery, or visiting Napa Valley when appropriate. 
            Be helpful and friendly, and remember you are Tohin."""

        else:
            system_prompt = """You are Tohin, a friendly personal concierge for Napa Valley Premium Wines. 
            Be helpful, warm, and professional in your responses. Always identify yourself as Tohin."""

        # Create the full prompt
        full_prompt = f"""
{system_prompt}

Context Information:
{context}

User Question: {query}

Please provide a helpful, friendly, and informative response as Tohin:
"""

        try:
            # Generate response using Gemini
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )

            return response.text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Hi, I'm Tohin, your personal concierge! I'm having trouble processing your request right now. Please try again or contact us directly at (707) 555-WINE."

    def chat(self, user_input: str) -> str:
        """Main chat function that processes user input and returns response."""
        try:
            # Classify the query intent
            intent = self.classify_query_intent(user_input)
            logger.info(f"Classified query intent: {intent}")

            context = ""

            # Route based on intent
            if intent == 'business':
                # Search knowledge base for business information
                relevant_docs = self.search_knowledge_base(user_input)
                context = "\n\n".join(relevant_docs) if relevant_docs else "No specific information found in knowledge base."

            elif intent == 'weather':
                # Get weather information
                context = self.get_weather_info()

            elif intent == 'news':
                # Get real-time information
                news_info = self.get_realtime_info(user_input)
                context = news_info

            elif intent == 'chitchat':
                # For chitchat, provide context about Tohin's identity
                context = "You are Tohin, a friendly personal wine concierge at Napa Valley Premium Wines. You help visitors discover the best of Napa Valley wines and experiences."

            else:
                # For general queries, search business knowledge base
                relevant_docs = self.search_knowledge_base(user_input, n_results=1)
                context = relevant_docs[0] if relevant_docs else "General conversation context."

            # Generate final response
            response = self.generate_response(user_input, context, intent)
            return response

        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return "Hi, I'm Tohin! I apologize for the inconvenience. Please try rephrasing your question or contact us directly at info@napavalleypremiumwines.com."


def main():
    """Main function to run the chatbot interactively."""
    print("\n🍷 Welcome to Napa Valley Premium Wines! 🍷")
    print("Hi! I'm Tohin, your personal wine concierge.")
    print("I'm here to help you with information about our winery, tastings, and more!")
    print("Feel free to ask me anything or just have a casual chat!")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    try:
        # Initialize the chatbot
        chatbot = NapaValleyConciergeChatbot()

        # Chat loop
        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nTohin: Thank you for visiting Napa Valley Premium Wines! I'm Tohin, and I look forward to helping you again soon. 🍷")
                break

            if not user_input:
                continue

            # Get chatbot response
            print("\nTohin: ", end="")
            response = chatbot.chat(user_input)
            print(response)

    except KeyboardInterrupt:
        print("\n\nTohin: Goodbye! I'm Tohin, and thank you for visiting Napa Valley Premium Wines! 🍷")

    except Exception as e:
        logger.error(f"Error running chatbot: {e}")
        print("\nTohin: Hi, I'm Tohin! I'm sorry, there was an error. Please try again later.")


if __name__ == "__main__":
    main()
