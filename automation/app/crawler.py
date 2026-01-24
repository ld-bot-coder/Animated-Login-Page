from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import logging

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, headless=False):
        self.headless = headless

    def crawl_url(self, url: str) -> dict:
        """
        Crawls a single URL and returns the text content.
        Uses Playwright to handle JS-heavy sites.
        """
        logger.info(f"Crawling: {url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            # Use a realistic user agent
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = context.new_page()
            
            try:
                # 30s timeout per page
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                # Basic cleaning: remove scripts, styles
                page.evaluate("""() => {
                    const elements = document.querySelectorAll('script, style, nav, footer, iframe, .ad, .ads');
                    elements.forEach(el => el.remove());
                }""")
                
                title = page.title()
                content = page.inner_text('body') # Get visible text
                
                browser.close()
                
                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "status": "success"
                }
                
            except Exception as e:
                logger.error(f"Failed to crawl {url}: {e}")
                browser.close()
                return {
                    "url": url,
                    "title": "",
                    "content": "",
                    "status": "error",
                    "error": str(e)
                }

    def crawl_many(self, urls: list) -> list:
        """
        Parallel crawling using ThreadPoolExecutor.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        # Limit max threads to avoid resource exhaustion (launching chromium per thread)
        max_workers = min(len(urls), 5) 
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.crawl_url, url): url for url in urls}
            for future in as_completed(future_to_url):
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    url = future_to_url[future]
                    logger.error(f"Thread failed for {url}: {e}")
                    results.append({
                        "url": url,
                        "status": "error",
                        "error": str(e)
                    })
                    
        return results
