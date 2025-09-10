🍷 Tohin - Napa Valley Wine Concierge Chatbot
<div align="center">
![Streamlit](https://img.shields.io/badge/Streame chatbot for Napa Valley Premium Wines**

Features - Installation - Usage - API Keys - Contributing

</div>
🌟 Features
🤖 Intelligent AI Conversations
Powered by Google Gemini AI for natural language understanding

Specialized wine knowledge and recommendations

Context-aware responses with personality

💬 ChatGPT-Style Interface
Modern, responsive dark-themed UI

Real-time message streaming

Conversation history management

Mobile and desktop optimized

🍷 Wine Expertise
Detailed wine recommendations and descriptions

Food pairing suggestions

Tasting notes and flavor profiles

Winery information and services

🌐 Real-Time Information
Live weather updates for Napa Valley

Current events and wine industry news

Dynamic content via Perplexity AI integration

📱 User Experience
Multiple conversation threads

Persistent chat history

One-click conversation management

Smooth scrolling and animations

🚀 Installation
Prerequisites
Python 3.8+ installed on your system

Git for cloning the repository

API keys from supported services (see API Setup)

Quick Setup
Clone the repository

bash
git clone https://github.com/tohin003/Task2.git
cd Task2
Install required packages

bash
pip install streamlit google-generativeai python-dotenv requests chromadb
Set up environment variables

bash
cp .env.example .env
# Edit .env file with your API keys
Run the application

bash
streamlit run app_ui.py
Open in browser

text
http://localhost:8501
🔑 API Setup
Required APIs
1. Google Gemini AI (Required)
Purpose: Main conversational AI engine

Get API Key: Google AI Studio

Free Tier: Yes (generous limits)

text
GEMINI_API_KEY=your_gemini_api_key_here
Optional APIs
2. Perplexity AI (Optional)
Purpose: Real-time information and current events

Get API Key: Perplexity API

Free Tier: Limited requests

text
PERPLEXITY_API_KEY=your_perplexity_api_key_here
3. OpenWeatherMap (Optional)
Purpose: Live weather data for Napa Valley

Get API Key: OpenWeatherMap

Free Tier: Yes (1000 calls/day)

text
WEATHER_API_KEY=your_openweathermap_api_key_here
🎯 Usage
Starting the Application
bash
# Development mode
streamlit run app_ui.py

# Production mode
streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0
Interacting with Tohin
Wine-Related Queries
text
• "What wines do you recommend for beginners?"
• "Tell me about your Cabernet Sauvignon Reserve"
• "What food pairs well with Pinot Noir?"
• "What are your tasting room hours?"
• "How much do wine tours cost?"
General Assistance
text
• "What's the weather like in Napa Valley?"
• "Tell me about yourself"
• "What's happening in the wine industry?"
• "Plan a wine tasting day for me"
Interface Features
➕ New Conversation: Start fresh chat threads

🗑️ Delete: Remove individual conversations

🗑️ Clear All: Reset entire chat history

Enter Key: Send messages quickly

Responsive Design: Works on all devices

🏗️ Project Structure
text
Task2/
├── 📄 app.py                 # Core chatbot logic and AI integration
├── 🎨 app_ui.py             # Streamlit UI with ChatGPT styling
├── 🔧 .env                  # Environment variables (not tracked)
├── 📋 .env.example          # Template for environment setup
├── 🚫 .gitignore           # Git ignore patterns
├── 📖 README.md            # This documentation
├── 📊 chroma_db/           # Vector database storage (auto-created)
└── 🗂️ __pycache__/         # Python cache files (auto-created)
🎨 Technical Architecture
Backend (app.py)
NapaValleyConciergeChatbot: Main chatbot class

Intent Classification: Routes queries to appropriate handlers

Context Management: Maintains conversation context

API Integration: Handles external service calls

Frontend (app_ui.py)
Streamlit Framework: Web application framework

Custom CSS: ChatGPT-inspired dark theme

Session Management: Persistent conversation state

Responsive Layout: Mobile-first design approach

Data Flow
text
User Input → Intent Classification → Context Retrieval → AI Generation → Response Display
🛠️ Development
Local Development
bash
# Clone and setup
git clone https://github.com/tohin003/Task2.git
cd Task2
pip install -r requirements.txt

# Run with debug logging
streamlit run app_ui.py --logger.level debug

# Run backend independently
python app.py
Adding Features
New Intent Types: Modify classify_query_intent() in app.py

UI Components: Update app_ui.py with new Streamlit elements

API Integrations: Add new service calls in respective methods

Styling: Modify CSS in the st.markdown() style block

Testing
bash
# Test chatbot backend
python -c "from app import NapaValleyConciergeChatbot; bot = NapaValleyConciergeChatbot(); print(bot.chat('Hello'))"

# Test UI components
streamlit run app_ui.py --server.headless true
📊 Performance & Limitations
Performance
Response Time: ~2-5 seconds (depends on API latency)

Concurrent Users: Limited by Streamlit's capabilities

Memory Usage: ~50-100MB base + conversation history

Current Limitations
Knowledge Cutoff: Limited to AI model training data

API Rate Limits: Depends on chosen service tiers

Single Instance: No multi-user session isolation

Data Persistence: Conversations lost on app restart

🔐 Security & Privacy
Data Handling
No Data Storage: Conversations are session-based only

API Key Protection: Environment variables and .gitignore

No Personal Data: No user authentication or data collection

Best Practices
Keep API keys in .env file only

Never commit sensitive information

Use HTTPS in production deployments

Regularly rotate API keys

🚢 Deployment
Streamlit Cloud (Free)
Push code to GitHub (without .env)

Connect repository to Streamlit Cloud

Add API keys in "Secrets" section

Deploy with one click

Heroku
bash
# Create Procfile
echo "web: streamlit run app_ui.py --server.port \$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
Docker
text
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_ui.py", "--server.port", "8501"]
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch

bash
git checkout -b feature/amazing-feature
Make your changes

Test thoroughly

Commit with clear messages

bash
git commit -m "Add: Amazing new feature description"
Push and create PR

bash
git push origin feature/amazing-feature
Contribution Guidelines
Follow existing code style and formatting

Add comments for complex logic

Update README if adding new features

Test with multiple conversation scenarios

Ensure mobile responsiveness for UI changes

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License - Feel free to use, modify, and distribute
Commercial use allowed with attribution
🙏 Acknowledgments
Technologies Used
Streamlit - Web application framework

Google Gemini AI - Conversational AI capabilities

Perplexity AI - Real-time information retrieval

ChromaDB - Vector database for embeddings

OpenWeatherMap - Weather data services

Inspiration
ChatGPT Interface - UI/UX design inspiration

Wine Industry Knowledge - Domain expertise integration

Conversational AI - Natural language processing advances

📞 Support & Contact
Getting Help
🐛 Issues: GitHub Issues

💬 Discussions: GitHub Discussions

📧 Email: Contact repository owner for support

Reporting Bugs
Please include:

Steps to reproduce

Expected vs actual behavior

Screenshots (for UI issues)

System information (OS, Python version)

Error logs (if applicable)

<div align="center">
Made with ❤️ for wine enthusiasts and AI lovers

⭐ Star this repository if you found it helpful! ⭐



</div>

Development and deployment guides

Contributing guidelines

Support information
