from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import asyncio 

class Crawler:
    def __init__(self, handler, start_domain=None, max_depth=2, concurrency=20):
        self.handler = handler
        self.start_domain = start_domain
        self.max_depth = max_depth
        self.semaphore = asyncio.Semaphore(concurrency)
        self.visited = set()
        self.results = []

    async def crawl(self, url, depth=0):
        if depth > self.max_depth:
            return
        
        if url in self.visited:
            return
        
        if self.start_domain:
            if urlparse(url).netloc != self.start_domain:
                return
        self.visited.add(url)
        async with self.semaphore:
            response = await self.handler.get(url)

        if not response or "text/html" not in response.headers.get("Content-Type", ""):
            return
        
        html = response.text

        #extract endpoints + params
        endpoints = self.extract_link(url, html)

        for endpoint, params in endpoints:
            self.results.append({
                "url" : endpoint,
                "params" : params
            })

        for endpoint, _ in endpoints:
            await self.crawl(endpoint, depth + 1)
        
    def extract_link(self, base_url, html):
        soup = BeautifulSoup(html, "html.parser")
        links = set()

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(base_url, href)

            #nomalize chi lay http/https
            parsed = urlparse(full_url)
            if parsed.scheme not in ["http", "https"]:
                continue

            #extract params    
            params = list(parse_qs(parsed.query).keys())

            #remove pragment 
            clean_url = parsed._replace(fragment="").geturl()

            links.add((clean_url, tuple(params)))
        return links
    async def run(self, start_urls):
        if not self.start_domain and start_urls:
            self.start_domain = urlparse(start_urls[0]).netloc
            
        tasks = [self.crawl(url) for url in start_urls]
        await asyncio.gather(*tasks)

        #remove duplicate
        unique = []
        seen = set()

        for item in self.results:
            key = item["url"]
            if key not in seen:
                seen.add(key)
                unique.append(item)

        return unique