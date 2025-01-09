# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import io
# import time
# import sys
# from webdriver_manager.chrome import ChromeDriverManager

# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# url = "https://www.instagram.com"

# username = "untuk_iir"
# password = "studyserver"

# def login_to_instagram(driver, username, password):
#     driver.get(url)
#     time.sleep(3)

#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")
#     username_input.send_keys(username)
#     password_input.send_keys(password)

#     password_input.send_keys(Keys.RETURN)
#     time.sleep(10)
    
#     try:
#         not_now_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
#         )
#         not_now_button.click()
#     except Exception as e:
#         print("No 'Not Now' button found or already dismissed.")


# def scroll_and_collect_captions(driver, scroll_count=5):
#     captions = set()

#     for _ in range(scroll_count):
#         posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")

#         for post in posts:
#             try:
#                 caption = post.text
#                 captions.add(caption)
#             except Exception as e:
#                 print(f"Error fetching caption: {e}")

#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)

#     return list(captions)

# def main():
#     try:
#         login_to_instagram(driver, username, password)

#         captions = scroll_and_collect_captions(driver, scroll_count=5)

#         for i, caption in enumerate(captions, start=1):
#             print(f"{i}:{caption}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
# if __name__ == "__main__":
#     main()

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

# Inisialisasi WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Atur encoding output ke UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# URL Instagram
url = "https://www.instagram.com"

# Akun Instagram
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

    # Klik tombol login
    password_input.send_keys(Keys.RETURN)
    time.sleep(10)

    # Tutup pop-up "Save Your Login Info" jika muncul
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        not_now_button.click()
    except Exception as e:
        print("No 'Not Now' button found or already dismissed.")

def scroll_and_collect_captions(driver, scroll_count=5):
    # Menggunakan set untuk memastikan deduplikasi
    unique_captions = set()

    for _ in range(scroll_count):
        # Ambil elemen caption dari postingan
        posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")

        for post in posts:
            try:
                # Ambil teks caption
                caption = post.text.strip()  # Hilangkan spasi tambahan
                if caption:  # Pastikan caption tidak kosong
                    unique_captions.add(caption)
            except Exception as e:
                print(f"Error fetching caption: {e}")

        # Scroll ke bawah untuk memuat lebih banyak konten
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # Kembalikan caption sebagai list unik
    return list(unique_captions)

def main():
    try:
        # Login ke Instagram
        login_to_instagram(driver, username, password)

        # Ambil caption dengan scroll
        captions = scroll_and_collect_captions(driver, scroll_count=5)

        # Cetak caption satu per satu
        for i, caption in enumerate(captions, start=1):
            print(f"{i}. {caption}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Tutup browser setelah selesai
        driver.quit()

if __name__ == "__main__":
    main()
