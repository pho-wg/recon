from urllib.parse import urlparse

class Analyzer:
    def __init__(self):
        self.sensitive_paths = ["admin", "login", "dashboard", "config"]
        self.sqli_params = ["id", "user", "uid", "account"]
        self.redirect_params = ["redirect", "url", "next"]
        self.file_params = ["file", "path", "page"]

    def analyze(self, crawled_data):
        findings = []
        
        for item in crawled_data:
            url = item["url"]
            params = item.get("param", [])

            parsed = urlparse(url)
            path = parsed.path.lower()

            result = {
                "url": url,
                "issues" : []
            }

            #sensitive path detection
            for keyword in self.sensitive_paths:
                if keyword in path:
                    result["issues"].append("sensitive_endponit")
            
            #sqli candidate 
            for p in params:
                if p.lower() in self.sqli_params:
                    result["issues"].append(f"possible_sqli_param:{p}")

            #open redirect candidate
            for p in params:
                if p.lower() in self.file_params:
                    result["issues"].append(f"possible_file_inclusion:{p}")

            #chi luu neu co issue
            if result["issues"]:
                findings.append(result)
        return findings