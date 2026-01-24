import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

def search_google(query: str, limit: int = 10, freshness: str = "1M"):
    """
    Execute a Realtime Google Search via Oxylabs.
    
    Args:
        query: Search term
        limit: Number of results (default 10)
        freshness: Time range (e.g., '1D', '1M', '1Y') - Not directly supported by all Oxy payloads easily without custom params, 
                   but we can try to inject if needed. Simplest is raw query.
    
    Returns:
        List of dicts: [{'url': ..., 'title': ..., 'snippet': ...}]
    """
    
    if not Config.OXYLABS_USERNAME or not Config.OXYLABS_PASSWORD:
        logger.error("Oxylabs credentials missing.")
        return []

    # Oxylabs Realtime Search Payload
    payload = {
        "source": "google_search",
        "domain": "com",
        "query": query,
        "parse": True,
        "limit": limit,
        # "context": [{"key": "tbs", "value": f"qdr:{freshness.lower()}"}] # Optional freshness if needed
    }

    try:
        response = requests.post(
            Config.OXYLABS_ENDPOINT,
            auth=(Config.OXYLABS_USERNAME, Config.OXYLABS_PASSWORD),
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        if 'results' in data and len(data['results']) > 0:
            content = data['results'][0].get('content', {})
            
            # 1. Extract Knowledge Graph / Answer Box / AI Overview (if available)
            # Oxylabs structure varies, but often 'knowledge_graph' or 'organic' > 'sitelinks' etc.
            # We'll look for specific keys that represent "Direct Answers"
            
            # Check for Knowledge Graph
            if 'knowledge_graph' in content:
                 kg = content['knowledge_graph']
                 title = kg.get('title') or kg.get('title_link', {}).get('title', 'Google Knowledge Graph')
                 desc = kg.get('description') or kg.get('desc', '') or str(kg)
                 results.append({
                     'url': kg.get('website', 'http://google.com'),
                     'title': f"[Google Direct] {title}",
                     'snippet': f"AI/Direct Answer: {desc}",
                     'is_direct_answer': True
                 })

            # Check for Answer Box (Featured Snippet)
            # Sometimes embedded in lists or top formatted results (ignored in basic loop usually)
            
            organic = content.get('results', {}).get('organic', [])
            
            for item in organic:
                results.append({
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'snippet': item.get('desc', '') or item.get('snippet', ''),
                    'is_direct_answer': False
                })
                
        logger.info(f"Oxylabs search returned {len(results)} results for query: {query}")
        return results

    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
