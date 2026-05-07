# Web Recon tool 
This automated web reconnaissance tool, built in Python, helps dectect potential security vulnerabilities through crawling and attack surface ananlysis

Features:

    Subdomain Enumeration: Lists subdomains via file or crt.sh
    Probing: Checks if the target is still active 
    Crawling: Collects all endpoints and parameters in the domain
    Analyzing: Dectects potential secrurity issues :
        - Sensitive Endpoint (/admin, /login, /config...)
        - Possible SQL Injection (?id=, ?uid=, ?nid=...)
        - Possible Open Redirect (?url=, ?redirect=...)
        - Possible File Inclusion (?file=, ?path=, ?content=...)
    Report: Saves results as JSON 

Tested on demo.testfire.net and DC-8 (vulhub)

Installation requirements: Python 3.10+

Install library:

    pip install httpx beautifulsoup4

Usage:

    #using a domain (via crt.sh)
    python3 main.py -d demo.testfire.com

    #using a subdomain file
    python3 main.py -f targets.txt

# Current limitations & future development directions:

  No JavaScript rendering support (SPAs like react, angular)
  
  No active testing support after login 
  
  Added HTML report export
  
  Integrated active SQLi testing
  
  Added CMS detection

# Disclaimer 

This tool is intended for education purposes and authorized security testing only 

  - Only use this tool on systems you **own** or have **explicit 
  written permission** to test
- Unauthorized use against systems you do not own is **illegal** 
  and unethical
- The author assumes **no responsibility** for any misuse or 
  damage caused by this tool
- Always follow responsible disclosure practices

