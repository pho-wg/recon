import httpx

class SubdomainEnumerator:
    def __init__(self, timeout=10):
        self.timeout = timeout

    #load subdomain tu file 
    def load(self, filepath):
        subdomains = set()

        try: 
            with open(filepath, "r") as f:
                for line in f :
                    sub = line.strip()
                    if sub:
                        subdomains.add(sub)
        except FileNotFoundError:
            print(f"[!] File not found: {filepath}")

        return list(subdomains)
    
    #lay them tu crt.sh (optional)
    async def fetch_crtsh(self, domain):
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        subdomains = set()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(url)

                if res.status_code != 200:
                    return []

                data = res.json()

                for entry in data:
                    names = entry.get("name_value", "")
                    for sub in names.split("\n"):
                        sub = sub.strip()
                        if domain in sub:
                            subdomains.add(sub)
        except Exception:
            return []
        return list(subdomains)
    
    #convert thanh url
    def to_urls(self, subdomains):
        urls = set()
        for sub in subdomains:
            sub = sub.strip()

            if not sub.startswith("http"):
                urls.add(f"http://{sub}")
                urls.add(f"https://{sub}")
            else:
                urls.add(sub)
        return list(urls)