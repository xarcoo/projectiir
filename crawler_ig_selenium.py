from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'comfydent.clothing'
PASSWORD = 'comfyajarek'

chrome_options = Options()
chrome_options.add_argument("--window-size=1520,800")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get("https://www.instagram.com/")

time.sleep(3)

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

password_input.send_keys(Keys.RETURN)
time.sleep(3)

if "https://www.instagram.com/" not in driver.current_url:
    print("Login failed. Check your credentials or CAPTCHA.")
else:
    def smooth_scroll_down(driver, scroll_step=300, delay=0.2, max_scroll=5000):
        scroll_height = 0
        while scroll_height < max_scroll:
            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(delay)
            scroll_height += scroll_step
    smooth_scroll_down(driver, scroll_step=200, delay=0.1, max_scroll=5000)

    posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")
    for post in posts:
        print(post.text)

driver.quit()