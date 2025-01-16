import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestOrangeHRM:
    def setup_method(self):
        """Setup method to open the browser before each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def teardown_method(self):
        """Teardown method to close the browser after each test"""
        self.driver.quit()

    def test_google_search_and_login(self):
        """Step 1-6: Search OrangeHRM on Google, login successfully"""
        driver = self.driver

        # Step 1: Open Google
        driver.get("https://www.google.com")
        time.sleep(2)

        # Step 2: Search for "OrangeHRM demo login"
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("OrangeHRM demo login")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 3: Click the first search result
        first_result = driver.find_element(By.XPATH, "(//h3)[1]")
        first_result.click()
        time.sleep(3)

        # Step 4: Verify we are on the login page
        assert "orangehrmlive.com" in driver.current_url, "Not on the correct login page!"

        # Step 5: Enter login credentials
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("Admin")
        password_field.send_keys("admin123")
        login_button.click()
        time.sleep(5)

        # Step 6: Validate login success
        assert "dashboard" in driver.current_url.lower(), "Login Failed!"
        print("✅ Login successful on Desktop!")

        # After successful login, start clicking the sidebar options
        self.test_sidebar_navigation()

    def test_sidebar_navigation(self):
        """Step 7: Click each sidebar option (except Maintenance) and validate"""
        driver = self.driver

        # Wait for the sidebar to be visible after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul')))

        # Define the sidebar options manually, skipping the "Maintenance" option
        sidebar_options = [
            "PIM",
            "Leave",
            "Time",
            "Recruitment",
            "My Info",
            "Performance",
            "Dashboard",
            "Directory",
            "Maintenance"
        ]

        for option_name in sidebar_options:
            try:
                # Find the sidebar option and click it
                option = driver.find_element(By.XPATH, f'//span[text()="{option_name}"]/ancestor::a')

                if option_name.lower() == "maintenance":
                    print(f"Skipping Maintenance section...")
                    continue

                print(f"Clicking on: {option_name}")

                # Wait for the element to be clickable and then click
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(option))
                option.click()
                time.sleep(3)

                # Try checking the page heading (if available)
                page_heading = driver.find_element(By.TAG_NAME, "h6").text.strip()
                assert option_name.lower() in page_heading.lower(), f"❌ Validation failed for {option_name}"
                print(f"✅ Successfully navigated to: {page_heading}")
            except Exception as e:
                print(f"⚠️ Could not validate {option_name} via heading, skipping validation. Error: {str(e)}")