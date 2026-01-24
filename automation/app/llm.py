import requests
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.api_key = Config.OLLAMA_API_KEY
        self.model = Config.LLM_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _generate(self, messages: list, stream: bool = False) -> str:
        url = f"{self.base_url}/v1/chat/completions" # Assuming OpenAI compat endpoint, else use /api/chat
        # Note: User provided curl used /api/chat. Let's switch to native /api/chat if that's what their curl used.
        # User curl: https://ollama.com/api/chat
        
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

        try:
            response = requests.post(
                url, 
                headers=self.headers, 
                json=payload, 
                timeout=120 # Synthetic reasoning takes time
            )
            response.raise_for_status()
            
            data = response.json()
            # Ollama /api/chat response structure
            if 'message' in data:
                 return data['message']['content']
            # Fallback for standard OpenAI format if they swap endpoints behind proxy
            if 'choices' in data:
                return data['choices'][0]['message']['content']
                
            return "Error: Unexpected response format from LLM provider."
            
        except Exception as e:
            logger.error(f"LLM Generation failed: {e}")
            return f"**Error Generating Answer**: The AI provider returned an error ({e}). Please check the sources below directly."

    def extract_entities(self, text: str) -> list:
        """
        Extract specific entities from text using LLM.
        """
        prompt = f"""
        Extract key medical/technical entities from the following text. 
        Return ONLY a JSON list of strings. No markdown, no conversation.
        
        Text: {text[:4000]} # Truncate to avoid context window issues
        """
        
        response = self._generate([
            {"role": "system", "content": "You are a precise data extraction engine. Output JSON only."},
            {"role": "user", "content": prompt}
        ])
        
        try:
            # Clean possible markdown code blocks
            clean_resp = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_resp)
        except:
            logger.warning(f"Failed to parse entities JSON: {response}")
            return []

    def synthesize_answer(self, query: str, sources: list) -> str:
        """
        Synthesize an answer based on crawled sources.
        """
        context_str = "\n\n".join([f"Source {i+1} ({s['url']}):\n{s['content'][:1500]}" for i, s in enumerate(sources)])
        
        prompt = f"""
        Query: {query}
        
        Using ONLY the provided sources, synthesize a comprehensive, factual answer.
        - Cite sources using [1], [2] notation.
        - If the query asks for specific fields (e.g., email, phone, address) or list of items, **YOU MUST OUTPUT A MARKDOWN TABLE**.
        - The table should have columns like Field/Attribute | Value | Source.
        - If conflict exists, note it.
        - Structure with headers if complex.
        
        Sources:
        {context_str}
        """
        
        return self._generate([
            {"role": "system", "content": "You are a helpful Research Assistant. Synthesize facts with strict citations."},
            {"role": "user", "content": prompt}
        ])
