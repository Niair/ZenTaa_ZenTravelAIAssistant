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
        except Exception:
            self.primary = False

    def query(self, prompt: str):
        system_message = "You are a helpful travel assistant. Keep responses concise and factual."
        if self.primary:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  # Lower temperature for more consistent responses
                max_tokens=150
            )
            return resp.choices[0].message.content
        else:
            try:
                # Try Ollama locally
                return ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])["message"]["content"]
            except Exception:
                # Fallback to Perplexity API
                headers = {
                    "Authorization": f"Bearer {Settings.PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                }
                data = {"model": "llama-3.1-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
                r = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=data)
                return r.json()["choices"][0]["message"]["content"]
