import time
import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class BunnySecurityTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.fake = Faker()
        # Standard path for chromedriver in Debian/Ubuntu PRoot
        self.driver_path = "/usr/bin/chromedriver"

    def _get_chrome_options(self):
        """Standard flags for running Chrome in a containerized environment."""
        opts = Options()
        opts.add_argument("--headless")  # Required: PRoot has no display
        opts.add_argument("--no-sandbox") # Required: Prevents permission errors
        opts.add_argument("--disable-dev-shm-usage") # Prevents memory crashes
        opts.add_argument("--incognito")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        
        # Professional User-Agent to simulate a desktop user
        opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        return opts

    def _create_session(self):
        """Clears session and initializes fresh driver."""
        if not os.path.exists(self.driver_path):
            logging.error(f"Driver not found at {self.driver_path}. Did you run 'apt install chromium-driver'?")
            sys.exit(1)
            
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=self._get_chrome_options())
        driver.delete_all_cookies() # Ensure fresh session
        return driver

    def run_cycle(self, cycle_num):
        driver = None
        try:
            driver = self._create_session()
            logging.info(f"Cycle {cycle_num}: Accessing target URL...")
            driver.get(self.target_url)

            # Generate Mock Data
            f_name = self.fake.first_name()
            l_name = self.fake.last_name()
            email = self.fake.email()
            password = self.fake.password(length=12, special_chars=True)

            wait = WebDriverWait(driver, 20)

            # --- Target Form Logic ---
            # Using XPATHs optimized for the provided registration link structure
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'First name')]"))).send_keys(f_name)
            driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Last name')]").send_keys(l_name)
            driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Email address')]").send_keys(email)
            driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Password')]").send_keys(password)

            logging.info(f"Submitting: {email}")
            
            # Locate and click the 'Create account' button
            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Create account')]")
            submit_btn.click()

            # Wait to capture potential rate-limit or success response
            time.sleep(5)
            logging.info(f"Cycle {cycle_num} Execution Complete.")

        except Exception as e:
            logging.error(f"Cycle {cycle_num} Error: {str(e)}")
        finally:
            if driver:
                driver.quit()

if __name__ == "__main__":
    TARGET = "TARGET_URL"
    
    print("--- Professional Automation Testing Tool (PRoot) ---")
    try:
        count = int(input("How many registration cycles to test? "))
        tester = BunnySecurityTester(TARGET)

        for i in range(1, count + 1):
            tester.run_cycle(i)
            # Short delay between cycles to avoid local CPU throttling
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProcess halted by user.")
    except ValueError:
        print("Please enter a valid number.")
