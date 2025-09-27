# send_whatsapp.py
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def send_whatsapp_message(phone: str, message: str, quantity: int = 1, profile_path: str = "./whatsapp_profile", headless: bool = False, timeout: int = 40):
    """
    phone: international format WITHOUT the +, e.g. "923001234567"
    message: text to send
    quantity: how many times to send the message
    profile_path: chrome user-data-dir to persist login/session
    """

    wa_url = f"https://web.whatsapp.com/send?phone={phone}&app_absent=0"

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")   # persist login
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(wa_url)
        wait = WebDriverWait(driver, timeout)

        # Wait for the chat box to load
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )

        for i in range(quantity):
            input_box.send_keys(message + Keys.ENTER)
            time.sleep(1)  # small delay between sends

        print(f"Message sent {quantity} times to {phone}.")

        # keep open a bit so you can see it worked
        time.sleep(3)

    except Exception as e:
        print("Error sending message:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    target_phone = input("Enter phone number (e.g. 923001234567): ")
    msg = input("Enter message to send: ")
    quan = int(input("How many times?: "))

    send_whatsapp_message(target_phone, msg, quantity=quan)
