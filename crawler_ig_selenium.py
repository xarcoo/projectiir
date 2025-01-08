from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'comfydent.clothing'
PASSWORD = 'comfyajarek'

unique_posts = set()

# Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start browser maximized

# Initialize WebDriver with ChromeDriverManager
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),  # Install and configure ChromeDriver
    options=chrome_options
)

# Open a webpage
driver.get("https://www.instagram.com/")
print(driver.title)  # Print the page title

time.sleep(3)  # Wait for the page to load

# Find username and password fields
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

# Enter credentials
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

# Submit login form
password_input.send_keys(Keys.RETURN)
time.sleep(5)  # Wait for login to complete

# Check if login was successful
if "https://www.instagram.com/" not in driver.current_url:
    print("Login failed. Check your credentials or CAPTCHA.")
else:
    print("Login successful!")

    # Navigate to the Instagram home page
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    def smooth_scroll_down(driver, scroll_step=300, delay=0.2, max_scroll=5000):
        scroll_height = 0
        while scroll_height < max_scroll:
            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(delay)
            scroll_height += scroll_step
    smooth_scroll_down(driver, scroll_step=200, delay=0.1, max_scroll=2000)

    posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")
    for post in posts:
        text = post.text
        if text not in unique_posts:
            unique_posts.add(text)
            print(text)

# Quit the driver
driver.quit()

