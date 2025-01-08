from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inisialisasi WebDriver (menggunakan ChromeDriver)
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL Instagram
url = "https://x.com/login"

# Akun Instagram (ganti dengan akun Anda)
username = "ar_chie__"
password = "S4P1kud4"

def login_to_twitter(driver, username, password):
    # Buka halaman login
    driver.get(url)
    time.sleep(15)

    # Masukkan username dan password
    username_input = driver.find_element(By.NAME, "text")

    username_input.send_keys(username)
    time.sleep(5)
    next = driver.find_element(By.CSS_SELECTOR, "button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
    next.click()
    time.sleep(5)
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    time.sleep(5)
    next = driver.find_element(By.CSS_SELECTOR, "span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3")
    next.click()
    
    # Submit login form
    time.sleep(10)

    # Handle "Save Your Login Info" pop-up


def scroll_and_collect_captions(driver, scroll_count=5):
    captions = set()  # Gunakan set untuk menghindari duplikasi

    for _ in range(scroll_count):
        # Ambil elemen posting (Caption)
        posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")

        for post in posts:
            try:
                # Ambil teks caption
                caption = post.text
                captions.add(caption)  # Tambahkan caption ke dalam set
            except Exception as e:
                print(f"Error fetching caption: {e}")

        # Scroll ke bawah menggunakan JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Tunggu untuk memuat konten tambahan

    return list(captions)  # Kembalikan sebagai list

def main():
    try:
        # Login ke Instagram
        login_to_twitter(driver, username, password)

        # Scroll dan ambil caption dari home feed
        captions = scroll_and_collect_captions(driver, scroll_count=5)

        # Tampilkan caption yang ditemukan
        for i, caption in enumerate(captions, start=1):
            print(f"{i}: {caption}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()