import socket
import requests
from bs4 import BeautifulSoup
import tldextract
import re

def extract_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def get_ip(hostname_or_ip):
    try:
        return socket.gethostbyname(hostname_or_ip)
    except socket.gaierror:
        print("[!] Invalid hostname or IP")
        return None

def find_subdomains(start_url, max_depth=1):
    visited = set()
    subdomains = set()

    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]

            base_domain = extract_domain(url)
            for link in links:
                if not link.startswith('http'):
                    continue
                link_domain = extract_domain(link)

                if link_domain == base_domain:
                    subdomain_match = re.match(r"https?://([a-zA-Z0-9.-]+)\." + re.escape(base_domain), link)
                    if subdomain_match:
                        subdomains.add(subdomain_match.group(1) + '.' + base_domain)

                    crawl(link, depth + 1)
        except Exception as e:
            pass  # optionally log

    crawl(start_url, 0)
    return subdomains

# --- Usage ---
if __name__ == "__main__":
    host_input = input("Enter hostname or IP: ").strip()

    ip = get_ip(host_input)
    if ip:
        start_url = f"http://{host_input}"
        print(f"[*] Crawling from {start_url}")
        found = find_subdomains(start_url)

        print("\n[+] Found Subdomains:")
        for sub in sorted(found):
            print(f" - {sub}")
