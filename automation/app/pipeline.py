import logging
import time
from app.search import search_google
from app.crawler import Crawler
from app.llm import OllamaClient
from config import Config

logger = logging.getLogger(__name__)

class SearchPipeline:
    def __init__(self):
        # User requested headless=False to see the browser action
        self.crawler = Crawler(headless=False)
        self.llm = OllamaClient()

    def run(self, query: str, deep_mode: bool = False):
        """
        Executes the full Search -> Reason -> Answer pipeline.
        
        Flow:
        1. Query -> Search (Oxylabs)
        2. Filter URLs
        3. Crawl Content (Playwright)
        4. Synthesize Answer (Ollama)
        """
        start_time = time.time()
        logger.info(f"Starting pipeline for query: {query}")
        
        # Step 1: Search
        search_limit = 5 if not deep_mode else 10
        search_results = search_google(query, limit=search_limit)
        
        if not search_results:
            return {
                "answer": "I could not find any relevant information from the web search.",
                "sources": [],
                "time_taken": time.time() - start_time
            }
            
        # Step 2: Separate Direct Answers from Crawl Targets
        direct_answers = [res for res in search_results if res.get('is_direct_answer', False)]
        crawl_targets = [res['url'] for res in search_results if not res.get('is_direct_answer', False) and res['url']]
        
        # Step 3: Crawl
        # Optimization: In deep mode, crawl all. In fast mode, maybe top 3.
        crawl_limit = 3 if not deep_mode else 8
        crawled_data = self.crawler.crawl_many(crawl_targets[:crawl_limit])
        
        # Filter successful crawls
        valid_sources = []
        
        # Add Google Direct Answers as high-confidence sources
        for item in direct_answers:
            valid_sources.append({
                "url": item.get('url', 'Google AI/Direct'),
                "title": item.get('title'),
                "content": f"GOOGLE HIGHLIGHT: {item.get('snippet')}",
                "status": "success"
            })

        # Add Crawled Pages
        valid_sources.extend([
            page for page in crawled_data 
            if page['status'] == 'success' and len(page['content']) > 100
        ])
        
        logger.info(f"Using {len(valid_sources)} valid sources ({len(direct_answers)} direct, {len(valid_sources)-len(direct_answers)} crawled)")
        
        if not valid_sources:
             return {
                "answer": "I found search results but could not access the page content to verify details.",
                "sources": search_results,
                "time_taken": time.time() - start_time
            }

        # Step 3: Synthesize
        answer = self.llm.synthesize_answer(query, valid_sources)
        
        return {
            "answer": answer,
            "sources": valid_sources,
            "search_metadata": search_results,
            "time_taken": time.time() - start_time
        }
