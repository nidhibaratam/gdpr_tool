import ssl
import socket
import csv
from datetime import datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# ---------------------------------
# Terminal Color Styling
# ---------------------------------
class Bcolors:
    CYAN = "\033[36m"
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# ---------------------------------
# Enhanced Banner
# ---------------------------------
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
    print(f"{Bcolors.BOLD}{Bcolors.CYAN}GDPR PRIVACY & SECURITY AUDITOR{Bcolors.RESET}")
    print(f"{Bcolors.BOLD}AUTHOR:{Bcolors.RESET} BARATAM NIDHISHRI")
    print(f"{Bcolors.BOLD}VERSION:{Bcolors.RESET} 1.0 (Integrity-Safe Engine)")
    print(f"{Bcolors.BOLD}ENGINE:{Bcolors.RESET} SSL | Cookie Provenance | Tracker Detection | Transparency Analysis")
    print(f"{Bcolors.BOLD}SCORING:{Bcolors.RESET} Weighted Multi-Dimensional Risk Quantification\n")
    print(f"{Bcolors.CYAN}" + "-" * 70 + f"{Bcolors.RESET}")


# ---------------------------------
# Core GDPR Compliance Engine
# ---------------------------------
def analyze_gdpr_compliance(url):
    report = {"score": 100, "findings": []}
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc.replace("www.", "")

    WEIGHTS = {
        "ssl": 0.30,
        "cookies": 0.20,
        "transparency": 0.25,
        "trackers": 0.25
    }

    GDPR_MAP = {
        "ssl": "GDPR Article 32 – Security of Processing",
        "cookies": "GDPR Articles 6 & 7 – Lawful Basis and Consent",
        "transparency": "GDPR Article 13 – Right to Information",
        "trackers": "GDPR Articles 6, 7 & 25 – Consent and Data Protection by Design"
    }

    risk_components = dict.fromkeys(WEIGHTS.keys(), 0)
    scan_successful = True

    print(f"{Bcolors.CYAN}[*] Validating Transport Security...{Bcolors.RESET}")

    # SSL Validation
    if parsed_url.scheme == "http":
        risk_components["ssl"] = 1
        report["findings"].append(
            f"{Bcolors.RED}Insecure Connection (HTTP used) "
            f"({GDPR_MAP['ssl']}){Bcolors.RESET}"
        )
    else:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname):
                    report["findings"].append(
                        f"{Bcolors.GREEN}HTTPS Transmission Secure "
                        f"({GDPR_MAP['ssl']}){Bcolors.RESET}"
                    )
        except Exception:
            risk_components["ssl"] = 1
            report["findings"].append(
                f"{Bcolors.RED}Invalid or Missing SSL Certificate "
                f"({GDPR_MAP['ssl']}){Bcolors.RESET}"
            )

    print(f"{Bcolors.CYAN}[*] Launching Browser-Based Inspection...{Bcolors.RESET}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            third_party_requests = set()

            def handle_request(request):
                req_domain = urlparse(request.url).netloc.replace("www.", "")
                if hostname and hostname not in req_domain:
                    third_party_requests.add(req_domain)

            page.on("request", handle_request)

            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(5000)

            # Cookie Analysis
            print(f"{Bcolors.CYAN}[*] Analyzing Cookies...{Bcolors.RESET}")

            cookies = context.cookies()
            first_party = 0
            third_party = 0

            for c in cookies:
                c_domain = c.get("domain", "").replace(".", "")
                if hostname in c_domain:
                    first_party += 1
                else:
                    third_party += 1

            total_cookies = len(cookies)

            if total_cookies > 0:
                cookie_risk = min((third_party * 0.1) + (first_party * 0.05), 1)
                risk_components["cookies"] = cookie_risk
                report["findings"].append(
                    f"Cookies Detected: {total_cookies} "
                    f"(First-Party: {first_party}, Third-Party: {third_party}) "
                    f"({GDPR_MAP['cookies']})"
                )
            else:
                report["findings"].append(
                    f"{Bcolors.GREEN}No cookies detected "
                    f"({GDPR_MAP['cookies']}){Bcolors.RESET}"
                )

            # Transparency Analysis
            print(f"{Bcolors.CYAN}[*] Checking Transparency Mechanisms...{Bcolors.RESET}")

            soup = BeautifulSoup(page.content(), 'html.parser')
            privacy_keywords = ["privacy", "policy", "data protection", "terms"]
            links = soup.find_all('a')

            has_policy = any(
                any(kw in (l.get_text().lower() + l.get('href', '').lower())
                    for kw in privacy_keywords)
                for l in links
            )

            if not has_policy:
                risk_components["transparency"] = 1
                report["findings"].append(
                    f"{Bcolors.RED}No Privacy Policy link detected "
                    f"({GDPR_MAP['transparency']}){Bcolors.RESET}"
                )
            else:
                report["findings"].append(
                    f"{Bcolors.GREEN}Privacy Policy link found "
                    f"({GDPR_MAP['transparency']}){Bcolors.RESET}"
                )

            # Tracker Detection
            print(f"{Bcolors.CYAN}[*] Inspecting Third-Party Network Requests...{Bcolors.RESET}")

            tracker_domains = [
                d for d in third_party_requests
                if any(x in d for x in
                       ["google", "facebook", "analytics", "doubleclick", "tracker"])
            ]

            if tracker_domains:
                tracker_risk = min(len(tracker_domains) * 0.2, 1)
                risk_components["trackers"] = tracker_risk
                report["findings"].append(
                    f"Third-Party Trackers Detected: {len(tracker_domains)} "
                    f"({GDPR_MAP['trackers']})"
                )
            else:
                report["findings"].append(
                    f"{Bcolors.GREEN}No major third-party trackers detected "
                    f"({GDPR_MAP['trackers']}){Bcolors.RESET}"
                )

            browser.close()

    except Exception:
        scan_successful = False
        report["findings"].append(
            f"{Bcolors.RED}Scan Error: Timed out or blocked by site.{Bcolors.RESET}"
        )

    if not scan_successful:
        report["score"] = None
        return report

    total_risk = sum(
        WEIGHTS[key] * risk_components[key]
        for key in WEIGHTS
    )

    final_score = round((1 - total_risk) * 100)
    report["score"] = max(0, final_score)
    report["legal_summary"] = list(GDPR_MAP.values())

    return report


# ---------------------------------
# Main Program
# ---------------------------------
def main():
    banner()

    print(f"{Bcolors.BOLD}HOW TO ENTER LINKS:{Bcolors.RESET}")
    print("example.com | www.example.com | https://example.com/page")
    print("-" * 70)

    user_input = input("ENTER WEBSITE URL: ").strip()

    # Reject malformed / HTML input
    if "<" in user_input or ">" in user_input or " " in user_input:
        print(f"{Bcolors.RED}Invalid URL format detected.{Bcolors.RESET}")
        return

    if not user_input.startswith(("http://", "https://")):
        user_input = "https://" + user_input

    parsed_test = urlparse(user_input)

    if not parsed_test.netloc or "." not in parsed_test.netloc:
        print(f"{Bcolors.RED}Invalid domain format. Please enter a valid website.{Bcolors.RESET}")
        return

    print(f"\n{Bcolors.CYAN}[*] Initiating Compliance Audit...{Bcolors.RESET}\n")

    result = analyze_gdpr_compliance(user_input)

    final_score = result['score']

    if final_score is None:
        print(f"\n{Bcolors.RED}AUDIT FAILED – No compliance score generated.{Bcolors.RESET}")
        return

    with open('audit_log.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            user_input,
            final_score
        ])

    print(f"\n{Bcolors.BOLD}FINAL COMPLIANCE SCORE: {final_score}/100{Bcolors.RESET}")
    print("-" * 70)

    for finding in result['findings']:
        print(finding)

    print(f"\n{Bcolors.BOLD}GDPR Articles Referenced:{Bcolors.RESET}")
    for article in set(result.get("legal_summary", [])):
        print(f" - {article}")

    print(f"\n{Bcolors.CYAN}Audit saved to audit_log.csv{Bcolors.RESET}\n")


if __name__ == "__main__":
    main()
