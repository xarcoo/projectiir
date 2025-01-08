from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import sys
import json

driver = webdriver.Chrome()

def login_twitter(username, password):
    """Login ke Twitter dengan akun yang diberikan."""
    driver.get("https://twitter.com/login")
    time.sleep(3)  # Tunggu halaman selesai dimuat

    # Cari elemen input username dan password
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.ENTER)
    time.sleep(2)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)  # Tunggu proses login selesai

    # Pastikan login berhasil
    if "login" in driver.current_url:
        print("Login gagal. Periksa username dan password Anda.")
        sys.exit(1)

def search_twitter(query, max_tweets=10):
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    driver.get(url)
    time.sleep(3)  # Tunggu halaman selesai dimuat
    
    tweets = []
    while len(tweets) < max_tweets:
        page_tweets = driver.find_elements(By.CSS_SELECTOR, "article div[lang]")
        for tweet in page_tweets:
            content = tweet.text
            if content not in tweets:  # Hindari duplikasi
                tweets.append(content)
            if len(tweets) >= max_tweets:
                break
        
        # Scroll ke bawah untuk memuat lebih banyak data
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    return tweets

if __name__ == '__main__':
    # Pastikan ada dua argumen: kata kunci dan jumlah hasil
    if len(sys.argv) < 3:
        print("Usage: python twitter_crawl.py <keyword> <max_results>")
        sys.exit(1)

    # Username dan password Twitter
    twitter_username = "TestIir17386"
    twitter_password = "testiir12"

    # Login ke Twitter
    print("Login ke Twitter...")
    login_twitter(twitter_username, twitter_password)

    keyword = sys.argv[1]
    max_results = int(sys.argv[2])

    # Pencarian tweet
    tweets = search_twitter(keyword, max_tweets=20)
    print(json.dumps(tweets))
    if not tweets:
        print("Tidak ada tweet yang ditemukan.")
        sys.exit()

    # Output hasil pencarian
    # for index, tweet in enumerate(tweets, start=1):
    #     print(f"\nTweet {index}:")
    #     print(f"Username: @{tweet['username']}")
    #     print(f"Tanggal: {tweet['created_at']}")
    #     print(f"Konten: {tweet['content']}")
