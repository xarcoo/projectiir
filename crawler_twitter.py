import tweepy
import sys

# Masukkan API keys Anda langsung di sini
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Autentikasi ke Twitter API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def search_tweets(query, count=5):
    """Mencari tweet berdasarkan kata kunci."""
    try:
        tweets = api.search_tweets(q=query, count=count, lang="id", tweet_mode="extended")
        results = []
        for tweet in tweets:
            results.append({
                'username': tweet.user.screen_name,
                'content': tweet.full_text,
                'created_at': tweet.created_at
            })
        return results
    except Exception as e:
        print(f"Terjadi kesalahan saat mencari tweet: {e}")
        return []

if __name__ == '__main__':
    # Pastikan ada dua argumen: kata kunci dan jumlah hasil
    if len(sys.argv) < 3:
        print("Usage: python twitter_crawl.py <keyword> <max_results>")
        sys.exit(1)

    keyword = sys.argv[1]
    max_results = int(sys.argv[2])

    # Pencarian tweet
    tweets = search_tweets(keyword, max_results)
    if not tweets:
        print("Tidak ada tweet yang ditemukan.")
        sys.exit()

    # Output hasil pencarian
    for index, tweet in enumerate(tweets, start=1):
        print(f"\nTweet {index}:")
        print(f"Username: @{tweet['username']}")
        print(f"Tanggal: {tweet['created_at']}")
        print(f"Konten: {tweet['content']}")
