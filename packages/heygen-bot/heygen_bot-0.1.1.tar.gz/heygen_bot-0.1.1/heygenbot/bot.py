from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class HeygenBot:
    """
    A bot to automate video creation tasks on Heygen using Selenium.

    Features:
    - Logs in using a session cookie
    - Navigates to the video creation interface
    - Automates script input, avatar selection, title setting, and video submission

    Usage:
    bot = HeygenBot(chromedriver_path, session_cookie_value)
    bot.login()
    bot.verify_login()
    bot.create_video(script_text, avatar_name="Karma", video_title="Demo")
    bot.close()
    """

    def __init__(self, chromedriver_path, session_cookie_value):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=self.options)
        self.cookie = {
            "name": "heygen_session",
            "value": session_cookie_value,
            "domain": ".heygen.com",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }

    def login(self):
        self.driver.get("https://www.heygen.com")
        time.sleep(2)
        self.driver.add_cookie(self.cookie)
        self.driver.get("https://app.heygen.com/home")
        print("✅ Logged in using heygen-session cookie.")

    def verify_login(self):
        try:
            verify_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify')]"))
            )
            verify_btn.click()
            print("✅ Clicked verify button")
        except:
            print("❌ No verify button found or already passed")

    def create_video(self, script_text, avatar_name="Karma", video_title="Task 12"):
        self.driver.get("https://app.heygen.com/create-v3/")
        print("✅ Opened Create Video page")
        time.sleep(2)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Script')]"))
            ).click()
            print("✅ Clicked on 'Scripts'")
        except Exception as e:
            print(f"❌ Failed to click on 'Scripts': {e}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add Script')]"))
            ).click()
            print("✅ Clicked on 'Add Script'")
        except Exception as e:
            print(f"❌ Failed to click on 'Add Script': {e}")

        try:
            editable_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            editable_box.click()
            editable_box.send_keys(Keys.CONTROL + "a")
            editable_box.send_keys(Keys.BACKSPACE)
            editable_box.send_keys(script_text)
            print("✅ Script added")
        except Exception as e:
            print(f"❌ Script input failed: {e}")

        for name in ["Avatar", avatar_name]:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{name}')]"))
                ).click()
                print(f"✅ Clicked on item containing '{name}'")
            except Exception as e:
                print(f"❌ Failed to click on '{name}': {e}")
        
        try:
            # Wait until an element containing 'Karma' is clickable
            karma_element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Hyper-Realistic')]"))
            )
            karma_element.click()
            print("✅ Clicked on item containing 'Video added'")
        except Exception as e:
            print(f"❌ Failed to click on 'Karma': {e}")  
        time.sleep(2)

        try:
            label_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Untitled Video')]"))
            )
            parent = label_element.find_element(By.XPATH, "..")
            try:
                input_box = parent.find_element(By.TAG_NAME, "input")
            except:
                input_box = parent.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
            input_box.click()
            input_box.send_keys(Keys.CONTROL + "a")
            input_box.send_keys(Keys.BACKSPACE)
            input_box.send_keys(video_title)
            print(f"✅ Video renamed to '{video_title}'")
        except Exception as e:
            print(f"❌ Failed to rename video: {e}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]"))
            ).click()
            print("✅ Clicked 'Submit'")
        except Exception as e:
            print(f"❌ Submit failed: {e}")

        try:
            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Submit Video')]"))
            )
            modal = popup.find_element(By.XPATH, "./ancestor::div[contains(@class, 'Dialog') or contains(@class, 'modal') or @role='dialog']")
            
            submit_button = modal.find_element(By.XPATH, ".//button[contains(., 'Submit')]")
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("✅ Confirmed 'Submit' in popup")
        except Exception as e:
            print(f"❌ Final submission failed: {e}")

    def close(self, delay=60):
        """
        Close the browser window after a specified delay.

        Parameters:
        delay (int or float): Number of seconds to wait before quitting the browser.
                             Set to 0 for immediate shutdown.
        """
        if delay > 0:
            time.sleep(delay)
        self.driver.quit()
