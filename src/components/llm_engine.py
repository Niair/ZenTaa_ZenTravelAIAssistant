import requests
import ollama
from groq import Groq
from config.settings import Settings


class LLMEngine:
    def __init__(self):
        try:
            self.client = Groq(api_key=Settings.GROQ_API_KEY)
            # ✅ Use latest Groq supported model
            self.model = "llama-3.1-8b-instant"
            self.primary = True
            print("✅ Groq LLM initialized successfully")
        except Exception as e:
            print(f"⚠️ Groq failed: {e}")
            self.primary = False

        # Define travel-specific system prompt
        self.travel_system_prompt = """You are Zen, a helpful and knowledgeable Travel AI Assistant specializing in India travel. 
        
Your role is to:
- Help users plan trips to India
- Provide destination recommendations
- Give travel tips, visa info, and cultural advice  
- Suggest itineraries, accommodations, and transportation
- Share information about Indian culture, food, and festivals
- Help with travel safety and health advice

Always respond in a friendly, helpful manner and focus on travel-related assistance. 
If asked about non-travel topics, politely redirect to travel planning."""

    def query(self, prompt: str):
        """Query the LLM with travel context"""
        if self.primary:
            try:
                # Add travel context to every query
                messages = [
                    {"role": "system", "content": self.travel_system_prompt},
                    {"role": "user", "content": prompt}
                ]
                
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500  # Reasonable response length
                )
                response = resp.choices[0].message.content
                
                # Log the interaction for debugging
                print(f"🔍 LLM Debug - Input: {prompt[:50]}...")
                print(f"🔍 LLM Debug - Output: {response[:100]}...")
                
                return response
            except Exception as e:
                print(f"❌ Groq API failed: {e}")
                return self._fallback_query(prompt)
        else:
            return self._fallback_query(prompt)
    
    def _fallback_query(self, prompt: str):
        """Fallback to other LLM services"""
        try:
            # Try Ollama locally first
            print("🔄 Trying Ollama fallback...")
            messages = [
                {"role": "system", "content": self.travel_system_prompt},
                {"role": "user", "content": prompt}
            ]
            response = ollama.chat(model="llama2", messages=messages)
            return response["message"]["content"]
        except Exception as ollama_error:
            print(f"⚠️ Ollama failed: {ollama_error}")
            try:
                # Fallback to Perplexity API
                print("🔄 Trying Perplexity fallback...")
                headers = {
                    "Authorization": f"Bearer {Settings.PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                }
                messages = [
                    {"role": "system", "content": self.travel_system_prompt},
                    {"role": "user", "content": prompt}
                ]
                data = {
                    "model": "llama-3.1-8b-instruct", 
                    "messages": messages,
                    "temperature": 0.7
                }
                r = requests.post("https://api.perplexity.ai/chat/completions", 
                                headers=headers, json=data)
                return r.json()["choices"][0]["message"]["content"]
            except Exception as perplexity_error:
                print(f"❌ All LLM services failed: {perplexity_error}")
                return "I'm sorry, I'm experiencing technical difficulties. Please try again later or check your API keys."

    def query_simple(self, prompt: str):
        """Simple query without travel context (for testing)"""
        if self.primary:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return resp.choices[0].message.content
        else:
            return self._fallback_query(prompt)


# Test the improved LLM
if __name__ == "__main__":
    print("=== TESTING IMPROVED TRAVEL LLM ===")
    llm = LLMEngine()
    
    # Test travel-focused responses
    test_prompts = [
        "Tell me a fun fact about India",  # Should now give travel-related India facts
        "I want to visit Delhi. What should I see?",
        "What's the weather like in India?",  # Should focus on travel implications
        "Hello, how are you?"  # Should introduce as travel assistant
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Prompt: {prompt}")
        response = llm.query(prompt)
        print(f"Response: {response}")
        print("-" * 50)