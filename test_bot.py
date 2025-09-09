"""
Test script to verify chatbot backend works independently
"""

from app import NapaValleyConciergeChatbot
import traceback

def test_chatbot():
    print("=== Testing Napa Valley Chatbot Backend ===\n")
    
    try:
        print("1. Initializing chatbot...")
        bot = NapaValleyConciergeChatbot()
        print("✅ Chatbot initialized successfully!\n")
        
        # Test different types of queries
        test_queries = [
            "Hello! Who are you?",
            "What wines do you offer?",
            "What's the weather like?",
            "Tell me about yourself"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"2.{i} Testing query: '{query}'")
            try:
                response = bot.chat(query)
                print(f"✅ Response: {response}\n")
            except Exception as e:
                print(f"❌ Error with query '{query}': {e}")
                traceback.print_exc()
                print()
        
        print("=== All tests completed ===")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()
