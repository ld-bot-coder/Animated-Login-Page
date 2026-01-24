import requests
import json
import time

BASE_URL = "http://localhost:5001/api/search"

queries = [
    "What is the customer support email for Airbnb?",
    "Find the contact phone number for Tesla roadside assistance.",
    "Address of Google headquarters in Mountain View",
    "What is the current stock price of Apple?",
    "Who is the CEO of Microsoft and can you find their public email?",
    "find email and phone of rahul kumar software developer working in multiplier ai hyderabad"
]

def test_search():
    print(f"Testing against {BASE_URL}...\n")
    
    for q in queries:
        print(f"Query: {q}")
        start = time.time()
        try:
            resp = requests.post(BASE_URL, json={"query": q, "deep_mode": False})
            resp.raise_for_status()
            data = resp.json()
            
            print(f"Status: {resp.status_code}")
            print(f"Time: {data.get('time_taken', 0):.2f}s")
            print(f"Answer: {data.get('answer', 'No answer')[:200]}...") # Truncate for readability
            print("-" * 50)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
