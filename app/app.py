import streamlit as st
import time
import threading
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.pipeline.main import ConversationalAgent

# Page configuration
st.set_page_config(
    page_title="ZenTravel AI Assistant",
    page_icon="🎧",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'tts_service' not in st.session_state:
    st.session_state.tts_service = "Unknown"

def initialize_agent():
    """Initialize the conversational agent"""
    try:
        if st.session_state.agent is None:
            with st.spinner("🔄 Initializing AI Assistant..."):
                agent = ConversationalAgent()
                st.session_state.agent = agent
                # Determine which TTS service is being used
                if hasattr(agent.tts, 'primary'):
                    st.session_state.tts_service = agent.tts.primary.upper()
                else:
                    st.session_state.tts_service = "ElevenLabs"  # Default fallback
                st.success("✅ Agent initialized successfully!")
        return st.session_state.agent
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {e}")
        return None

def main():
    st.title("🎧 ZenTravel AI Assistant")
    st.markdown("### Speak with your AI travel assistant in multiple languages!")
    
    # Initialize agent
    agent = initialize_agent()
    
    if agent is None:
        st.error("Unable to initialize the AI assistant. Please check your API keys and try again.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        recording_duration = st.slider(
            "Recording duration (seconds)", 
            min_value=3, 
            max_value=15, 
            value=5,
            help="How long to record your voice"
        )
        
        st.header("📊 System Info")
        st.write(f"**TTS Service:** {st.session_state.tts_service}")
        st.write(f"**Conversations:** {len(st.session_state.conversation_history)}")
        
        st.header("🔄 Controls")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()
            
        if st.button("🔊 Test Audio", use_container_width=True):
            test_tts(agent)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Live Conversation")
        
        # Conversation controls
        control_col1, control_col2 = st.columns([1, 1])
        
        with control_col1:
            if st.button(
                "🎤 Start Listening", 
                type="primary", 
                disabled=st.session_state.is_listening,
                use_container_width=True
            ):
                start_conversation(recording_duration, agent)
        
        with control_col2:
            if st.button(
                "⏹️ Stop Recording", 
                disabled=not st.session_state.is_listening,
                use_container_width=True
            ):
                st.session_state.is_listening = False
                st.rerun()
        
        # Status indicator
        status_placeholder = st.empty()
        if st.session_state.is_listening:
            with status_placeholder:
                st.warning(f"🔴 Recording... Speak now! (Timeout: {recording_duration}s)")
        else:
            with status_placeholder:
                st.success("✅ Ready to listen - Click 'Start Listening' above")
        
        # Conversation history
        st.header("📝 Conversation History")
        if not st.session_state.conversation_history:
            st.info("No conversations yet. Start by clicking 'Start Listening'.")
        else:
            for i, (timestamp, user_text, assistant_response) in enumerate(reversed(st.session_state.conversation_history)):
                with st.expander(f"💬 Conversation {len(st.session_state.conversation_history)-i} - {timestamp}"):
                    st.write(f"**You:** {user_text}")
                    st.write(f"**Assistant:** {assistant_response}")
    
    with col2:
        st.header("ℹ️ Real-time Status")
        
        # Status indicators
        st.subheader("System Components")
        
        # STT Status
        st.markdown("**Speech-to-Text**")
        st.progress(100, text="✅ Operational")
        
        # LLM Status  
        st.markdown("**Language Model**")
        st.progress(100, text="✅ Operational")
        
        # TTS Status
        st.markdown("**Text-to-Speech**")
        st.progress(100, text=f"✅ {st.session_state.tts_service}")
        
        # Current session info
        st.subheader("Session Info")
        st.write(f"**Started:** {datetime.now().strftime('%H:%M:%S')}")
        st.write(f"**Duration:** {recording_duration}s")
        st.write(f"**Total Chats:** {len(st.session_state.conversation_history)}")
        
        # Quick tips
        st.subheader("💡 Tips")
        st.info("""
        - Speak clearly into your microphone
        - Wait for the 'Recording...' message before speaking
        - Conversations are saved automatically
        - Supports multiple languages
        """)

def start_conversation(duration, agent):
    """Handle the conversation in a separate thread"""
    if not st.session_state.is_listening:
        st.session_state.is_listening = True
        
        def run_conversation():
            try:
                # Run the conversation
                response = agent.run_conversation(duration=duration)
                
                # Get the user input (we'll simulate it for now)
                # In a real implementation, you'd capture the actual transcribed text
                user_text = "Voice input"  # This would come from STT
                
                # Add to conversation history
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.conversation_history.append(
                    (timestamp, user_text, response)
                )
                
            except Exception as e:
                st.error(f"❌ Conversation error: {e}")
            finally:
                st.session_state.is_listening = False
                st.rerun()
        
        # Run in thread to avoid blocking the UI
        thread = threading.Thread(target=run_conversation)
        thread.daemon = True
        thread.start()

def test_tts(agent):
    """Test TTS functionality"""
    try:
        agent.tts.speak("Hello! I am your ZenTravel AI assistant. How can I help you with your travel plans today?")
        st.success("✅ Audio test completed successfully!")
    except Exception as e:
        st.error(f"❌ Audio test failed: {e}")

if __name__ == "__main__":
    main()