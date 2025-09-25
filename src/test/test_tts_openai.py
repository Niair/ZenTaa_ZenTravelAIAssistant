# ttsopenai_investigator.py
import requests
import json

def investigate_ttsopenai():
    """Investigate how TTSOpenAI's API actually works"""
    
    API_KEY = input("Enter your TTSOpenAI API key: ").strip()
    
    if not API_KEY or API_KEY == "tts-....":
        print("❌ Please enter your actual API key")
        return
    
    print("\n🔍 Investigating TTSOpenAI API structure...")
    
    # Test 1: Check if it's a webhook-based service
    print("\n1. Testing webhook pattern...")
    webhook_urls = [
        "https://api.ttsopenai.com/webhook/tts",
        "https://api.ttsopenai.com/api/tts",
        "https://api.ttsopenai.com/generate",
        "https://api.ttsopenai.com/v1/generate",
    ]
    
    for url in webhook_urls:
        try:
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"text": "test", "voice": "alloy"},
                timeout=10
            )
            print(f"   {url}: Status {response.status_code}")
            if response.status_code != 404:
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   {url}: Error - {e}")
    
    # Test 2: Check dashboard for API documentation link
    print("\n2. Checking for API documentation...")
    dashboard_urls = [
        "https://api.ttsopenai.com/docs",
        "https://docs.ttsopenai.com",
        "https://ttsopenai.com/documentation",
    ]
    
    for url in dashboard_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   📖 Documentation found at: {url}")
        except:
            pass
    
    # Test 3: Check what's in the webhook section
    print("\n3. Webhook investigation...")
    print("   Your profile shows 'Webhook' and 'Webhook history'")
    print("   This suggests TTSOpenAI might work by:")
    print("   - You configure a webhook URL where you receive audio")
    print("   - You send text to their API")
    print("   - They process it and send audio to your webhook")
    
    # Test 4: Simple GET request to check available endpoints
    print("\n4. Checking available endpoints...")
    base_url = "https://api.ttsopenai.com"
    endpoints = ["/", "/health", "/status", "/api", "/v1", "/webhook"]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"   GET {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   GET {endpoint}: Error - {e}")

def check_service_alternatives():
    """Suggest alternatives since TTSOpenAI API is unclear"""
    print("\n" + "="*50)
    print("📋 RECOMMENDATION")
    print("="*50)
    print("Since TTSOpenAI's API structure is not clear, I recommend:")
    print("1. Check your TTSOpenAI dashboard for API documentation")
    print("2. Look for 'API Examples' or 'Integration Guide'")
    print("3. Contact TTSOpenAI support for API details")
    print("4. Meanwhile, use ElevenLabs which has a clear API:")
    print("   - Well-documented")
    print("   - Reliable")
    print("   - High-quality voices")
    print("5. Your ElevenLabs integration is already working! ✅")

if __name__ == "__main__":
    investigate_ttsopenai()
    check_service_alternatives()