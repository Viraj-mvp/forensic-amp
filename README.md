🔊 Forensic-Amp: Attacker-Aware Log Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![PySide6](https://img.shields.io/badge/GUI-PySide6-blue)
![Focus](https://img.shields.io/badge/Focus-Digital%20Forensics-red)

> "What if Winamp was a SOC tool?"
🧠 Automated Threat Detection (The "Attacker Matrix")
Forensic-Amp is a GUI-based Digital Forensics Log Analyzer It automates the ingestion of server logs to reconstruct attacker activity, identifying specific kill-chain phases like **Brute Force**, **Privilege Escalation**, and **Data Exfiltration**.


## ⚡ Key Features

 1. 🧠 Automated Threat Detection (The "Attacker Matrix")
Instead of just displaying logs, Forensic-Amp applies logic to detect specific patterns:
- Brute Force Detection: Correlates multiple failed SSH login attempts from a single IP.
- Root Compromise: Flags successful logins to the root account immediately following failed attempts.
- Web Exploitation: Uses Regex to identify SQL Injection (SQLi) and Directory Traversal attempts in web logs.
 
 2. 📊 The "Frequency Analyzer" (Visualization)

- Timeline Visualization: Visualizes the density of attacks over time using interactive charts.
- Interactive: Filter events by clicking on specific clusters or IP addresses.

3. 💾 Investigator-First Design
- Forensically Safe: Operates in "Read-Only" mode. It does not alter the original log files.
- Report Generation: Auto-generates a natural language summary of the incident for non-technical stakeholders.

---

4. Tech Stack
- GUI Framework: PySide6 (Qt for Python) with custom "Winamp" styling.
- Backend Logic: Python (Standard Library) for high-speed log parsing.
- Visualization: PyQtGraph for real-time charting.

---

5. Installation & Usage

- Option A: Standalone Executable (Windows)
No Python installation required.
1. Download the latest `ForensicAmp.exe` from the Releases page.
2. Double-click to launch.
3. Drag and drop your log files  into the "Drop Zone".

- Option B: Run from Source

1. Clone the Repository**
```bash
git clone https://github.com/Viraj-mvp/forensic-amp.git
cd forensic-amp
```

2. Install Dependencies**
```bash
pip install -r requirements.txt
```

3. Run the Application**
```bash
python main.py
```

 Option C: Build it Yourself
Create your own executable using the included build script:
```bash
python build.py
```
The executable will be created in the `dist/` folder.
