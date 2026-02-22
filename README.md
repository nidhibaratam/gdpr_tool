# GDPR Privacy & Security Auditor

A lightweight Python-based tool designed to perform preliminary technical audits of websites against core GDPR compliance indicators, including transport security, cookie behavior, third-party tracking, and transparency mechanisms.

---

## Project Objective

This project aims to develop an automated technical compliance assessment engine that evaluates observable privacy and security indicators of public websites. It maps technical findings to relevant GDPR provisions and generates a weighted risk score.

The tool serves as a preliminary compliance risk indicator and does not constitute legal certification.

---

## How It Works

The auditor evaluates the following components:

### 1. SSL Certificate Validation  
Verifies whether HTTPS is properly configured and whether certificates are valid.  
Mapped to GDPR Article 32 – Security of Processing.

### 2. Cookie Analysis  
Detects first-party and third-party cookies set during page load.  
Mapped to GDPR Articles 6 & 7 – Lawful Basis and Consent.

### 3. Transparency Detection  
Searches for visible privacy policy or legal information links.  
Mapped to GDPR Article 13 – Right to Information.

### 4. Tracker Detection  
Monitors third-party network requests and identifies common analytics or tracking domains.  
Mapped to GDPR Articles 6, 7 & 25 – Consent and Data Protection by Design.

A weighted scoring model aggregates risk components and generates a final compliance score out of 100.

---
## System Architecture

The auditor follows a sequential inspection pipeline:
```code
+-------------------+
|   User Input URL  |
+---------+---------+
          |
          v
+-------------------+
| URL Normalization |
| & Validation      |
+---------+---------+
          |
          v
+------------------------------+
| Transport Security Analyzer  |
| - SSL handshake              |
| - Certificate validation     |
+---------+--------------------+
          |
          v
+--------------------------------------+
| Browser Inspection Engine (Playwright)
| - Headless Chromium session         |
| - Network interception              |
| - DOM rendering                     |
+---------+----------------------------+
          |
          v
+----------------------+   +-----------------------+
| Cookie Analyzer      |   | Tracker Detector     |
| - First-party count  |   | - Third-party domains|
| - Third-party count  |   | - Heuristic matching |
+----------+-----------+   +-----------+-----------+
           |                           |
           +-------------+-------------+
                         |
                         v
                +------------------+
                | Transparency     |
                | Scanner (HTML)   |
                | - Privacy links  |
                +--------+---------+
                         |
                         v
                +------------------+
                | Weighted Risk    |
                | Scoring Engine   |
                +--------+---------+
                         |
                         v
                +------------------+
                | Compliance Score |
                | (0 – 100)        |
                +--------+---------+
                         |
                         v
                +------------------+
                | CSV Audit Logger |
                +------------------+
```

### Risk Scoring Model
The compliance score is calculated using a weighted multi-dimensional risk aggregation model.

Each risk component produces a normalized risk value between 0 (no risk) and 1 (maximum risk).

#### Risk Components and Weights

|Component|	Weight	|Description|
|---|---|---|
SSL Security | 	0.30 |	Evaluates HTTPS usage and certificate validity |
Cookie Behavior|	0.20 |	Assesses first-party and third-party cookie presence |
Transparency	|0.25	| Detects presence of privacy policy or legal disclosure links |
Tracker Activity |	0.25	| Detects third-party tracking domains via network inspection |
Total Weight | 1.00


### Risk Calculation Formula

**Let:**
* $R_i$ = normalized risk value for component $i$
* $W_i$ = weight assigned to component $i$

**Total Risk**
$$\text{Total Risk} = \sum (W_i \times R_i)$$

**Final Compliance Score**
$$\text{Compliance Score} = (1 - \text{Total Risk}) \times 100$$


##### Score Interpretation

- **90–100** → Low observable technical risk  
- **70–89** → Moderate technical risk  
- **50–69** → Elevated compliance concerns  
- **Below 50** → High observable compliance risk  
---

## Features

- Weighted compliance scoring (0–100 scale)
- SSL certificate verification
- Cookie classification (first-party vs third-party)
- Heuristic tracker detection
- Transparency keyword scanning
- Local CSV logging of audit results
- Cross-platform compatibility (macOS, Windows, Linux)
- Browser automation powered by Playwright

---

## Requirements

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection for live site analysis

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nidhibaratam/gdpr_tool
cd gdpr_tool
```
### 2. Create and Activate Virtual Environment
macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows
```PowerShell
python -m venv venv
.\venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
python3 -m playwright install chromium
```
---

## Usage
### Run the auditor:
```bash
python audit.py
```

---

## Sample Simulation:

```code
   ____ ____  ____  ____                      _                     
  / ___|  _ \|  _ \|  _ \    __ _ _ __   __ _| |_   _ _______ _ __  
 | |  _| | | | |_) | |_) |  / _` | '_ \ / _` | | | | |_  / _ \ '__| 
 | |_| | |_| |  __/|  _ <  | (_| | | | | (_| | | |_| |/ /  __/ |    
  \____|____/|_|   |_| \_\  \__,_|_| |_|\__,_|_|\__, /___\___|_|    
                                                |___/                
    
GDPR PRIVACY & SECURITY AUDITOR
AUTHOR: BARATAM NIDHISHRI
VERSION: 1.0 (Integrity-Safe Engine)
ENGINE: SSL | Cookie Provenance | Tracker Detection | Transparency Analysis
SCORING: Weighted Multi-Dimensional Risk Quantification

----------------------------------------------------------------------
HOW TO ENTER LINKS:
example.com | www.example.com | https://example.com/page
----------------------------------------------------------------------
ENTER WEBSITE URL: https://github.com/nidhibaratam/gdpr_tool

[*] Initiating Compliance Audit...

[*] Validating Transport Security...
[*] Launching Browser-Based Inspection...
[*] Analyzing Cookies...
[*] Checking Transparency Mechanisms...
[*] Inspecting Third-Party Network Requests...

FINAL COMPLIANCE SCORE: 88/100
----------------------------------------------------------------------
HTTPS Transmission Secure (GDPR Article 32 – Security of Processing)
Cookies Detected: 6 (First-Party: 0, Third-Party: 6) (GDPR Articles 6 & 7 – Lawful Basis and Consent)
Privacy Policy link found (GDPR Article 13 – Right to Information)
No major third-party trackers detected (GDPR Articles 6, 7 & 25 – Consent and Data Protection by Design)

GDPR Articles Referenced:
 - GDPR Articles 6, 7 & 25 – Consent and Data Protection by Design
 - GDPR Article 13 – Right to Information
 - GDPR Article 32 – Security of Processing
 - GDPR Articles 6 & 7 – Lawful Basis and Consent

Audit saved to audit_log.csv

```

---

## Project Structure
```bash
gdpr_tool/
│
├── audit.py           # Main compliance engine
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT License
├── README.md          # Documentation
└── .gitignore         # Excludes venv and audit logs
```

---

## Legal Context
This project references the following GDPR provisions:

Article 32 – Security of Processing

Articles 6 & 7 – Lawful Basis and Consent

Article 13 – Transparency and Information

Article 25 – Data Protection by Design

The system performs automated technical observation and scoring. It does not replace formal legal audits or compliance certification processes.

----

## Limitations
- Transparency detection is keyword-based and does not evaluate policy content quality.

- Tracker detection uses heuristic matching and may not identify advanced obfuscation.

- Headless browser automation may be blocked by certain websites.

- The tool does not evaluate internal data handling, retention policies, or organizational compliance procedures.

- This is a prototype intended for academic and research purposes.

---

## License
Distributed under the MIT License.
Copyright (c) 2026 Baratam Nidhishri.
