import streamlit as st
from app import NapaValleyConciergeChatbot
import logging
import time
from datetime import datetime

# Set page config first
st.set_page_config(
    page_title="Tohin - Napa Valley Wine Concierge", 
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@st.cache_resource
def init_chatbot():
    """Initialize chatbot with error handling."""
    try:
        return NapaValleyConciergeChatbot()
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return None

# Initialize chatbot
chatbot = init_chatbot()

if chatbot is None:
    st.error("❌ Unable to start the chatbot. Please refresh the page or contact support.")
    st.stop()

# Initialize session state
if "conversations" not in st.session_state:
    st.session_state["conversations"] = {}
if "current_conversation_id" not in st.session_state:
    st.session_state["current_conversation_id"] = None
if "conversation_counter" not in st.session_state:
    st.session_state["conversation_counter"] = 0

def create_new_conversation():
    """Create a new conversation."""
    st.session_state["conversation_counter"] += 1
    conversation_id = f"conversation_{st.session_state['conversation_counter']}"
    st.session_state["conversations"][conversation_id] = {
        "title": "New Conversation",
        "messages": [],
        "created_at": datetime.now()
    }
    st.session_state["current_conversation_id"] = conversation_id
    return conversation_id

def get_current_conversation():
    """Get current conversation or create new one."""
    if (st.session_state["current_conversation_id"] is None or 
        st.session_state["current_conversation_id"] not in st.session_state["conversations"]):
        create_new_conversation()
    return st.session_state["conversations"][st.session_state["current_conversation_id"]]

def update_conversation_title(conversation_id, first_message):
    """Update conversation title based on first message."""
    if len(first_message) > 30:
        title = first_message[:30] + "..."
    else:
        title = first_message
    st.session_state["conversations"][conversation_id]["title"] = title

# ChatGPT-style CSS with compact welcome screen
st.markdown("""
<style>
    /* Import Inter font like ChatGPT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App Container */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #343541;
    }
    
    /* Remove Streamlit padding */
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    /* Sidebar Styling - Dark theme like ChatGPT */
    .css-1d391kg {
        background-color: #202123 !important;
        width: 260px !important;
    }
    
    .sidebar .sidebar-content {
        background-color: #202123 !important;
        padding: 0 !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        padding: 16px 12px;
        border-bottom: 1px solid #444654;
    }
    
    .sidebar-title {
        color: white;
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    
    .sidebar-subtitle {
        color: #8e8ea0;
        font-size: 12px;
        font-weight: 400;
    }
    
    /* New Chat Button - ChatGPT Style */
    .new-chat-btn {
        margin: 8px 12px 16px 12px;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #4f4f4f 0%, #404040 100%) !important;
        color: white !important;
        border: 1px solid #565869 !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: all 0.1s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(180deg, #5a5a5a 0%, #4a4a4a 100%) !important;
        border-color: #6b7280 !important;
    }
    
    /* Conversation History Area */
    .conversation-history {
        flex: 1;
        overflow-y: auto;
        padding: 0 12px;
    }
    
    .conversation-history h3 {
        color: #8e8ea0 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        margin: 16px 0 8px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Individual Conversation Items */
    .conversation-item {
        display: flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 2px 0;
        cursor: pointer;
        transition: background-color 0.1s ease;
        group: hover;
    }
    
    .conversation-item:hover {
        background-color: #2a2b32;
    }
    
    .conversation-item.active {
        background-color: #343541;
    }
    
    /* Conversation buttons */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #ececf1 !important;
        border: none !important;
        text-align: left !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        width: 100% !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: background-color 0.1s ease !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #2a2b32 !important;
    }
    
    /* Delete buttons */
    .delete-btn {
        color: #8e8ea0;
        background: none;
        border: none;
        padding: 4px;
        border-radius: 4px;
        cursor: pointer;
        opacity: 0;
        transition: all 0.1s ease;
    }
    
    .conversation-item:hover .delete-btn {
        opacity: 1;
    }
    
    .delete-btn:hover {
        color: #f87171;
        background-color: rgba(248, 113, 113, 0.1);
    }
    
    /* Sidebar Footer */
    .sidebar-footer {
        padding: 16px 12px;
        border-top: 1px solid #444654;
        margin-top: auto;
    }
    
    /* Clear History Button */
    .clear-history-btn .stButton > button {
        background: transparent !important;
        color: #8e8ea0 !important;
        border: 1px solid #444654 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: all 0.1s ease !important;
    }
    
    .clear-history-btn .stButton > button:hover {
        background-color: #2a2b32 !important;
        color: #ececf1 !important;
    }
    
    /* Main Chat Area */
    .main-chat-container {
        background-color: #343541;
        min-height: 0px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding-bottom: 100px;
    }
    
    /* Message Styling */
    .message-container {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px 0;
    }
    
    .message-container.user {
        background-color: #343541;
    }
    
    .message-container.assistant {
        background-color: #444654;
    }
    
    .message-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 24px;
        display: flex;
        gap: 24px;
    }
    
    .message-avatar {
        width: 30px;
        height: 30px;
        border-radius: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 4px;
    }
    
    .message-avatar.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
    }
    
    .message-avatar.assistant {
        background-color: #10a37f;
        color: white;
        font-weight: 600;
    }
    
    .message-text {
        flex: 1;
        color: #ececf1;
        font-size: 16px;
        line-height: 1.75;
        word-wrap: break-word;
    }
    
    .message-text p {
        margin: 0 0 16px 0;
    }
    
    .message-text p:last-child {
        margin-bottom: 0;
    }
    
    /* Welcome Screen - COMPACT VERSION */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 120px;
        text-align: center;
        padding-left: 24px;
        padding-right: 24px;
        min-height: 400px;
    }
    
    .welcome-title {
        color: #ececf1;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    .welcome-subtitle {
        color: #8e8ea0;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 8px;
    }
    
    .welcome-description {
        color: #8e8ea0;
        font-size: 16px;
        font-weight: 400;
    }
    
    /* Input Container - Fixed at bottom like ChatGPT */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 260px;
        right: 0;
        background-color: #343541;
        padding: 24px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
    }
    
    .input-wrapper {
        max-width: 800px;
        margin: 0 auto;
        position: relative;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #40414f !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ececf1 !important;
        font-size: 16px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 16px 50px 16px 16px !important;
        width: 100% !important;
        box-shadow: 0 0 0 2px transparent !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8e8ea0 !important;
    }
    
    /* Send Button */
    .send-button {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #10a37f;
        border: none;
        border-radius: 8px;
        color: white;
        padding: 8px 12px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .send-button:hover {
        background-color: #0d8168;
    }
    
    .send-button:disabled {
        background-color: #555;
        cursor: not-allowed;
    }
    
    /* Hide Streamlit elements */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .css-18ni7ap, footer {
        display: none !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .input-container {
            left: 0;
            padding: 16px;
        }
        
        .message-content {
            padding: 0 16px;
            gap: 16px;
        }
        
        .css-1d391kg {
            width: 100% !important;
        }
        
        .welcome-screen {
            padding-top: 80px;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR - ChatGPT Style
with st.sidebar:
    # Header
    st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">🍷 Tohin</div>
            <div class="sidebar-subtitle">Napa Valley Wine Concierge</div>
        </div>
    """, unsafe_allow_html=True)
    
    # New Conversation Button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕ New Conversation", use_container_width=True, key="new_conv", type="primary"):
        create_new_conversation()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation History
    st.markdown('<div class="conversation-history">', unsafe_allow_html=True)
    st.markdown("### Recent Conversations")
    
    if st.session_state["conversations"]:
        for conv_id, conv_data in reversed(list(st.session_state["conversations"].items())):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                button_type = "primary" if conv_id == st.session_state["current_conversation_id"] else "secondary"
                if st.button(conv_data["title"], key=f"conv_{conv_id}", use_container_width=True, type=button_type):
                    st.session_state["current_conversation_id"] = conv_id
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                    if conv_id in st.session_state["conversations"]:
                        del st.session_state["conversations"][conv_id]
                        if conv_id == st.session_state["current_conversation_id"]:
                            if st.session_state["conversations"]:
                                st.session_state["current_conversation_id"] = list(st.session_state["conversations"].keys())[-1]
                            else:
                                st.session_state["current_conversation_id"] = None
                    st.rerun()
    else:
        st.markdown('<p style="color: #8e8ea0; font-size: 14px; padding: 12px; text-align: center;">No conversations yet</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar Footer with Clear Button
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    st.markdown('<div class="clear-history-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Clear All Conversations", use_container_width=True, key="clear_all"):
        st.session_state["conversations"] = {}
        st.session_state["current_conversation_id"] = None
        st.session_state["conversation_counter"] = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# MAIN CHAT AREA
current_conversation = get_current_conversation()

# Main container
st.markdown('<div class="main-chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

if current_conversation["messages"]:
    # Display messages ChatGPT style
    for i, message in enumerate(current_conversation["messages"]):
        if message["is_user"]:
            st.markdown(f"""
                <div class="message-container user">
                    <div class="message-content">
                        <div class="message-avatar user">U</div>
                        <div class="message-text">
                            <p>{message['content']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="message-container assistant">
                    <div class="message-content">
                        <div class="message-avatar assistant">T</div>
                        <div class="message-text">
                            <p>{message['content']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Compact Welcome screen
    st.markdown("""
        <div class="welcome-screen">
            <div class="welcome-title">👋 Welcome! I'm Tohin</div>
            <div class="welcome-subtitle">Your personal wine concierge at Napa Valley Premium Wines</div>
            <div class="welcome-description">How can I help you today?</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# FIXED INPUT AT BOTTOM - ChatGPT Style
st.markdown("""
    <div class="input-container">
        <div class="input-wrapper">
""", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "",
        placeholder="Send a message to Tohin...",
        label_visibility="collapsed",
        key="chat_input"
    )
    submitted = st.form_submit_button("Send", use_container_width=False)

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Process user input
if submitted and user_input.strip():
    # Add user message
    current_conversation["messages"].append({
        "content": user_input,
        "is_user": True,
        "timestamp": datetime.now()
    })
    
    # Update conversation title if it's the first message
    if len(current_conversation["messages"]) == 1:
        update_conversation_title(st.session_state["current_conversation_id"], user_input)
    
    # Get bot response
    try:
        with st.spinner("Tohin is thinking..."):
            response = chatbot.chat(user_input)
        
        if not response or not response.strip():
            response = "I'm sorry, I didn't generate a proper response. Please try asking again."
    except Exception as e:
        response = "I apologize, but I'm having trouble processing your request right now. Please try again."
        logger.error(f"Chat error: {e}")
    
    # Add bot response
    current_conversation["messages"].append({
        "content": response,
        "is_user": False,
        "timestamp": datetime.now()
    })
    
    st.rerun()
