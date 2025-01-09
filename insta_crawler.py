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

# # Inisialisasi WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

# # Atur encoding output ke UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # URL Instagram
# url = "https://www.instagram.com"

# # Akun Instagram
# username = "comfydent.clothing"
# password = "comfyajarek"

# def login_to_instagram(driver, username, password):
#     # Buka halaman login
#     driver.get(url)
#     time.sleep(3)

#     # Masukkan username dan password
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")
#     username_input.send_keys(username)
#     password_input.send_keys(password)

#     # Klik tombol login
#     password_input.send_keys(Keys.RETURN)
#     time.sleep(10)

#     # Tutup pop-up "Save Your Login Info" jika muncul
#     try:
#         not_now_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
#         )
#         not_now_button.click()
#     except Exception as e:
#         print("No 'Not Now' button found or already dismissed.")

# def scroll_and_collect_captions(driver, scroll_count=3):
#     # Menggunakan set untuk memastikan deduplikasi
#     unique_captions = set()

#     for _ in range(scroll_count):
#         # Ambil elemen caption dari postingan
#         posts = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")

#         for post in posts:
#             try:
#                 # Ambil teks caption
#                 caption = post.text.strip()  # Hilangkan spasi tambahan
#                 if caption:  # Pastikan caption tidak kosong
#                     unique_captions.add(caption)
#             except Exception as e:
#                 print(f"Error fetching caption: {e}")

#         # Scroll ke bawah untuk memuat lebih banyak konten
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)

#     # Kembalikan caption sebagai list unik
#     return list(unique_captions)

# def main():
#     try:
#         # Login ke Instagram
#         login_to_instagram(driver, username, password)

#         # Ambil caption dengan scroll
#         captions = scroll_and_collect_captions(driver, scroll_count=5)

#         # Cetak caption satu per satu
#         for i, caption in enumerate(captions, start=1):
#             print(f"{i}. {caption}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         # Tutup browser setelah selesai
#         driver.quit()

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
import sys,pyautogui
from webdriver_manager.chrome import ChromeDriverManager

# Inisialisasi WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Atur encoding output ke UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# URL Instagram
url = "https://www.instagram.com"

# Akun Instagram
username = "comfydent.clothing"
password = "comfyajarek"

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
    time.sleep(4)

    # Tutup pop-up "Save Your Login Info" jika muncul
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        not_now_button.click()
    except Exception as e:
        print("No 'Not Now' button found or already dismissed.")

def go_to_explore(driver):
    try:
        # Cari tombol Explore
        explore_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Explore']")
        
        # Klik tombol Explore
        explore_button.click()
        time.sleep(5)  # Tunggu halaman Explore termuat
    except Exception as e:
        print(f"Error clicking explore button: {e}")

def collect_captions_from_posts(driver, max_posts=10):
    captions = []

    try:
        # Klik postingan pertama di halaman Explore
        first_post = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aagw"))
        )
        first_post.click()
        time.sleep(5)

        for _ in range(max_posts):
            try:
                # Ambil caption dari postingan
                caption_element = driver.find_element(By.CSS_SELECTOR, "h1._ap3a._aaco._aacu._aacx._aad7._aade")
                caption = caption_element.text
                print(f"Captured Caption: {caption}")
            except Exception as e:
                print(f"Error fetching caption: {e}")

            # Tekan tombol next untuk pindah ke postingan berikutnya
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
        # Login ke Instagram
        login_to_instagram(driver, username, password)

        # Pergi ke halaman Explore
        go_to_explore(driver)

        # Ambil caption dari postingan
        captions = collect_captions_from_posts(driver, max_posts=10)

        # Cetak caption
        for i, caption in enumerate(captions, start=1):
            print(f"{i}. {caption}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Tutup browser setelah selesai
        driver.quit()

if __name__ == "__main__":
    main()

