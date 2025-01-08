from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inisialisasi WebDriver (menggunakan ChromeDriver)
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL Instagram
url = "https://www.instagram.com"

# Akun Instagram (ganti dengan akun Anda)
username = "untuk_iir"
password = "studyserver"

def login_to_instagram(driver, username, password):
    # Buka halaman login
    driver.get(url)
    time.sleep(3)

    # Masukkan username dan password
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Submit login form
    password_input.send_keys(Keys.RETURN)
    time.sleep(10)

    # Handle "Save Your Login Info" pop-up
    
    try:
        # Tunggu hingga tombol "Not Now" muncul
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        not_now_button.click()
        print("Clicked 'Not Now' button.")
    except Exception as e:
        print("No 'Not Now' button found or already dismissed.")


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
        login_to_instagram(driver, username, password)

        # Scroll dan ambil caption dari home feed
        captions = scroll_and_collect_captions(driver, scroll_count=5)

        # Tampilkan caption yang ditemukan
        for i, caption in enumerate(captions, start=1):
            print(f"{caption}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()

