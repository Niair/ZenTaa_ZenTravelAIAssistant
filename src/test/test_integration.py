#!/usr/bin/env python3
"""
Test script to verify STT → LLM → TTS integration
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_integration():
    """Test the complete integration"""
    print("🧪 Testing ZenTravel AI Integration...")
    
    try:
        # Test individual components first
        print("\n1. Testing LLM component...")
        from src.components.llm_engine import LLMEngine
        llm = LLMEngine()
        test_response = llm.query("Say 'Integration test' in a creative way")
        print(f"✅ LLM test passed: {test_response[:100]}...")
        
        print("\n2. Testing STT component...")
        from src.components.stt import STT
        stt = STT()
        print("✅ STT initialization passed")
        
        print("\n3. Testing TTS component...")
        from src.components.tts import TTS
        tts = TTS()
        print("✅ TTS initialization passed")
        
        print("\n4. Testing TTS speaking...")
        tts.speak("Integration test successful! The system is working properly.")
        print("✅ TTS speaking test passed")
        
        print("\n5. Testing complete agent...")
        from src.pipeline.main import ConversationalAgent
        agent = ConversationalAgent()
        print("✅ Agent initialization passed")
        
        print("\n🎉 All integration tests passed! The system is ready.")
        print("\nNext steps:")
        print("1. Run 'python src/pipeline/main.py' for CLI conversation")
        print("2. Run 'streamlit run app/streamlit_app.py' for web interface")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_integration()