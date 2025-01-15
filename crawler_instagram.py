from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import io
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "https://www.instagram.com"

username = "comfydent.clothing"
password = "comfyajarek"

def login_to_instagram(driver, username, password):
    driver.get(url)
    time.sleep(3)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)
    time.sleep(4)

    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        not_now_button.click()
    except Exception as e:
        print("No 'Not Now' button found or already dismissed.")

def go_to_explore(driver):
    try:
        explore_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Explore']")
        
        explore_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error clicking explore button: {e}")

def collect_captions_from_posts(driver, max_posts=10):
    captions = []

    try:
        first_post = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aagw"))
        )
        first_post.click()
        time.sleep(5)

        for _ in range(max_posts):
            try:
                caption_element = driver.find_element(By.CSS_SELECTOR, "h1._ap3a._aaco._aacu._aacx._aad7._aade")
                caption = caption_element.text
                print(f"Captured Caption: {caption}")
            except Exception as e:
                print(f"Error fetching caption: {e}")

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Next']"))
                )
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print("No 'Next' button found or could not click.")
                break
    except Exception as e:
        print(f"Error opening post: {e}")

    return captions

def main():
    try:
        login_to_instagram(driver, username, password)
        time.sleep(4)

        go_to_explore(driver)

        captions = collect_captions_from_posts(driver, max_posts=10)

        for i, caption in enumerate(captions, start=1):
            print(f"{i}. {caption}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

