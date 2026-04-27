import httpx

class RequestHandler:
    # hàm gửi yêu cầu có thể tự động chueyern hướng
    def __init__(self, timeout=5):
        self.client = httpx.AsyncClient(
            timeout = timeout,
            follow_redirects = True,
            headers = {
                "User-Agent":"Mozillla/5.0(ReconTool)"
            }
        )
    
    # hàm lấy dữ liệu từ 1 địa chỉ url 
    async def get(self, url):
        try: 
            response = await self.client.get(url)
            return response
        except httpx.RequestError:
            return None

    #hàm gửi dữ liệu lên máy chủ    
    async def post(self, url, data = None):
        try:
            response = await self.client.post(url, data=data)
            return response
        except httpx.RequestError:
            return None
    
    #đóng kết nối của client
    async def close(self):
        await self.client.aclose()