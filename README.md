# 🛡️ Account Creation Security Auditor (ACSA)
**Environment:** Python | Selenium | Termux (PRoot-Debian)

## 📌 Project Overview
This tool is designed for **authorized penetration testing** and security auditing of organization-specific registration endpoints. The primary goal is to evaluate the effectiveness of:
* **Anti-Automation Mechanisms:** Testing for the presence of CAPTCHAs or bot detection.
* **Rate Limiting:** Identifying the threshold of requests allowed before IP/Session blocking.
* **Session Management:** Verifying if cookies and session data are correctly invalidated after registration attempts.

## 🚀 Technical Features
* **Full Session Isolation:** Each test cycle clears all cookies and utilizes a unique Incognito browser instance.
* **Realistic Data Generation:** Uses the `Faker` library to generate unique, varied user profiles (Name, Email, Password) to bypass basic pattern detection.
* **Termux/PRoot Optimized:** Specifically configured to run Chromium in a headless, sandboxed environment on ARM64 hardware.
* **Automated Scaling:** Allows the operator to define the exact number of cycles for stress-testing.

## 🛠️ Installation & Setup
To run this tool within a **PRoot Debian** environment on Termux:

### 1. System Requirements
```bash
# Update repositories
apt update && apt upgrade

# Install browser dependencies
apt install chromium chromium-driver python3 python3-pip -y

***credit: T_Y😎***