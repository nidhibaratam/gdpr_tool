import ssl
import socket
import csv
from datetime import datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class Bcolors:
    CYAN = "\033[36m"
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def banner():
    art = r"""
  ____ ____  ____  ____                      _                    
 / ___|  _ \|  _ \|  _ \    __ _ _ __   __ _| |_   _ _______ _ __ 
| |  _| | | | |_) | |_) |  / _` | '_ \ / _` | | | | |_  / _ \ '__|
| |_| | |_| |  __/|  _ <  | (_| | | | | (_| | | |_| |/ /  __/ |   
 \____|____/|_|   |_| \_\  \__,_|_| |_|\__,_|_|\__, /___\___|_|   
                                               |___/             
    """
    print(f"{Bcolors.CYAN}{art}{Bcolors.RESET}")
    print(f"\t{Bcolors.BOLD}AUTHOR: BARATAM NIDHISHRI | VERSION: 1.0 (Stable Release){Bcolors.RESET}\n")
    
def analyze_gdpr_compliance(url):
    report = {"score": 100, "findings": []}
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    # 1. SSL Validation (Fixed for all host types)
    if parsed_url.scheme == "http":
        report["score"] -= 30
        report["findings"].append(f"{Bcolors.RED}❌ Insecure Connection (HTTP used){Bcolors.RESET}")
    else:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    report["findings"].append(f"{Bcolors.GREEN}✅ HTTPS Transmission Secure{Bcolors.RESET}")
        except Exception:
            report["score"] -= 30
            report["findings"].append(f"{Bcolors.RED}❌ Invalid or Missing SSL Certificate{Bcolors.RESET}")

    # 2. Browser Scan with User-Agent Spoofing
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using a real-world User-Agent to prevent bot blocking
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        context = browser.new_context(user_agent=user_agent, ignore_https_errors=True)
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4000) # Wait 4 seconds for trackers to load
            
            # --- Cookie Analysis ---
            cookies = context.cookies()
            num_c = len(cookies)
            if num_c > 0:
                penalty = 40 if num_c > 20 else (20 if num_c > 5 else 10)
                report["score"] -= penalty
                report["findings"].append(f"⚠️ {num_c} cookies set: Penalty -{penalty}")
            
            # --- Transparency Analysis ---
            soup = BeautifulSoup(page.content(), 'html.parser')
            privacy_keywords = ["privacy", "protection", "legal", "policy", "cookies", "terms", "confidentialité"]
            links = soup.find_all('a')
            has_policy = any(any(kw in (l.get_text().lower() + l.get('href', '').lower()) for kw in privacy_keywords) for l in links)
            
            if not has_policy:
                report["score"] -= 30
                report["findings"].append(f"{Bcolors.RED}❌ No Privacy Policy link detected (-30){Bcolors.RESET}")
            else:
                report["findings"].append(f"{Bcolors.GREEN}✅ Privacy Policy link found{Bcolors.RESET}")

            # --- Web Beacon Analysis ---
            beacons = soup.find_all(['img', 'script'], src=lambda s: s and ("pixel" in s or "track" in s or "analytics" in s))
            if len(beacons) > 0:
                b_penalty = min(len(beacons) * 10, 30)
                report["score"] -= b_penalty
                report["findings"].append(f"⚠️ {len(beacons)} trackers detected: Penalty -{b_penalty}")

        except Exception:
            report["findings"].append(f"{Bcolors.RED}❌ Scan Error: Timed out or blocked by site.{Bcolors.RESET}")
        finally:
            browser.close()
    return report

def main():
    banner()

    print(f"{Bcolors.BOLD}HOW TO ENTER LINKS:{Bcolors.RESET}")
    print(f" - Standard:  {Bcolors.CYAN}example.com{Bcolors.RESET} or {Bcolors.CYAN}www.example.com{Bcolors.RESET}")
    print(f" - Full URL:  {Bcolors.CYAN}https://example.com/page{Bcolors.RESET}")
    print(f" - Formatted: {Bcolors.CYAN}printf(\"https:// www.example.com ||\"}}{Bcolors.RESET} (Auto-cleaned)")
    print("-" * 60)
    user_input = input("ENTER WEBSITE URL: ").strip()
    if not (user_input.startswith("http://") or user_input.startswith("https://")):
        user_input = "https://" + user_input
    
    print(f"\n{Bcolors.CYAN}[*] Running Nominal Audit...{Bcolors.RESET}")
    result = analyze_gdpr_compliance(user_input)
    
    final_score = max(0, result['score'])
    with open('audit_log.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), user_input, final_score])

    print(f"\n{Bcolors.BOLD}FINAL COMPLIANCE SCORE: {final_score}/100{Bcolors.RESET}")
    print("-" * 60)
    for f in result['findings']: print(f)
    print(f"\n{Bcolors.CYAN}[!] Audit saved to audit_log.csv{Bcolors.RESET}\n")

if __name__ == "__main__":
    main()
