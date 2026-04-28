import asyncio
import argparse
import json

from utils.request_handler import RequestHandler
from modules.subdomain import SubdomainEnumerator
from modules.probe import prober
from modules.crawler import Crawler
from modules.analyzer import Analyzer
from urllib.parse import urlparse as _parse

async def run(domain=None, sub_file=None):
    print ("[+] Starting Recon Pipeline... \n")

    handler = RequestHandler()
    
    #subdomain enumeration
    enum = SubdomainEnumerator()
    subdomains = []
    if sub_file:
        print("[+] Loading subdomains from file...")
        subdomains = enum.load(sub_file)

    elif domain:
        print("[+] Fetching subdomains from crt.sh...")
        subs = await enum.fetch_crtsh(domain)
        subdomains = subs
    
    else: 
        print("[!] No input provided (domain or file).")
        return
    
    if not subdomains:
        print("[!] No subdomains found")
        return
    
    urls = enum.to_urls(subdomains)
    print(f"[+] Total targets: {len(urls)}\n")

    #probe (alive check)
    print("[+] Probing targets...")
    pr0ber = prober(handler)
    prober_results = await pr0ber.run(urls)

    alive_urls = [r["url"] for r in prober_results if r["status"] < 500]

    print(f"[+] Alive targets: {len(alive_urls)}\n")
    if not alive_urls:
        print("[!] No alive targets. Exiting.")
        await handler.close()
        return
    
    #crawling
    print("[+] Crawling...")
    crawler = Crawler(handler, max_depth=2)
    crawled_data = await crawler.run(alive_urls)

    print(f"[+] Crawled endpoints: {len(crawled_data)} \n")

    #analyze
    print("[+] Analyzing attack surface...")
    target_domain = _parse(alive_urls[0]).hostname
    analyzer = Analyzer(target_domain=target_domain)
    findings = analyzer.analyze(crawled_data)

    print(f"[+] Findings: {len(findings)} \n")

    #save report
    output = {
        "targets": alive_urls,
        "endpoint": crawled_data,
        "findings": findings
    }

    with open("result.json", "w") as f:
        json.dump(output, f, indent=4)
    
    print("[+] Report saved to result.json")
    await handler.close()

def main():
    parser = argparse.ArgumentParser(description="Simple Recon Tool")

    parser.add_argument("-d", "--domain", help="Target domain (example.com)")
    parser.add_argument("-f", "--file", help="Subdomain file input")

    args = parser.parse_args()
    asyncio.run(run(domain=args.domain, sub_file=args.file))
if __name__ == "__main__":
    main()