# check xem web song hay chet
from bs4 import BeautifulSoup
import asyncio

class prober:
    # khởi tạo và quản lý tài nguyên 
    #dùng self để đại diện cho đối tượng trong (oop) để nó vẫn xác định được khi sang hàm khác
    def __init__(self, handler, concurrency=20):
        self.handler = handler
        self.semaphore = asyncio.Semaphore(concurrency)

    # gửi yêu cầu và xử lý dữ liệu fetch 
    async def fetch(self, url):
        # giới hạn 20 nên nếu có 20 request thì phải đợi 
        async with self.semaphore:
            response = await self.handler.get(url)

            if not response:
                return None
            
            title = self.extract_title(response.text)

            return {
                "url" : url,
                "status" : response.status_code,
                "title" : title
            }
    
    # trích xuất tiêu đề 
    def extract_title(self, html):
        try:
            #phân tích cú pháp html và tìm thẻ title 
            soup = BeautifulSoup(html, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                return title_tag.text.strip()
        except Exception:
            pass
        return ""
    
    #điều phối quá trình 
    async def run(self, urls):
        tasks = [self.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks)

        #loc bo none
        return [r for r in results if r]