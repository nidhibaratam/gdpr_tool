# 🛡️ GDPR Privacy & Security Auditor

A lightweight Python tool to audit websites for GDPR compliance basics, including SSL security, tracking density, and transparency.

## 📊 How it works
The auditor analyzes:
- **SSL Certificate Validity:** Checks for secure HTTPS connections.
- **Cookie Density:** Detects cookies set before user consent.
- **Transparency:** Scans for Privacy Policy or Legal links.
- **Trackers:** Identifies web beacons and analytics scripts.

---

## 🛠️ Features
- **Scoring System:** 0–100 points with automated penalties for issues.
- **CSV Logging:** Results are saved locally to `audit_log.csv` (Private & GDPR-compliant).
- **Cross-Platform:** Works on macOS, Windows, and Linux.
- **Async Performance:** Powered by Playwright for fast, reliable scanning.

---

## ⚡ Requirements
- **Python 3.9+**
- **pip** (Python package manager)
- **Internet Connection** (to scan live sites)

---

## 📝 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/nidhibaratam/gdpr_tool
cd gdpr_tool
```

### 2. Set up Virtual Environment
macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python3 -m playwright install chromium
```

## 🧪 Usage
Run the auditor and enter any URL when prompted:
```bash
python audit.py
```

## 🖥️ Sample Terminal Output

```bash
 ____ ____  ____  ____                      _                    
/ ___|  _ \|  _ \|  _ \    __ _ _ __   __ _| |_   _ _______ _ __ 
| |  _| | | | |_) | |_) |  / _` | '_ \ / _` | | | | |_  / _ \ '__|
| |_| | |_| |  __/|  _ <  | (_| | | | | (_| | | |_| |/ /  __/ |   
 \____|____/|_|   |_| \_\  \__,_|_| |_|\__,_|_|\__, /___\___|_|   
                                               |___/              

AUTHOR: BARATAM NIDHISHRI | VERSION: 1.0 (Stable Release)

HOW TO ENTER LINKS:
example.com or www.example.com or https://example.com/page
------------------------------------------------------------
ENTER WEBSITE URL: https://github.com/nidhibaratam/gdpr_tool

[*] Running Nominal Audit...

FINAL COMPLIANCE SCORE: 80/100
------------------------------------------------------------
✅ HTTPS Transmission Secure
⚠️ 6 cookies set: Penalty -20
✅ Privacy Policy link found

[!] Audit saved to audit_log.csv
```

## 📂 Project Structure

```
gdpr_tool/
│
├── audit.py           # Main execution logic & CSV logging
├── LICENSE            # Distributed under the MIT License
├── requirements.txt   # Project dependencies (Playwright, BeautifulSoup4)
├── README.md          # Project documentation
└── .gitignore         # Excludes venv/ and audit_log.csv
```

## 📜 License
Distributed under the MIT License. See LICENSE for more information.
Author: BARATAM NIDHISHRI

### 🚀 How to update this on your GitHub:
1. Copy the code above.
2. Run `nano README.md` in your terminal.
3. Delete the old text and paste this in.
4. Press `Control+O`, `Enter`, then `Control+X` to save.
5. Push to GitHub:
```bash
git add README.md
git commit -m "Clean up and format README"
git push origin main
```
