import requests
import sys

# Masukkan API key YouTube Anda di sini
instagram_api_key = 'EAATGnmSyGI4BOwKmFbeAXUCT4V1wrkwfMTcgOfqo6aVgc9M4vPe658CIXnuXx0EZCeUTUZCVRZCIJZBjkUdKntX655P4Qlzof8ZCyB3Hmhu1cgW7q4MZCFVMY322T9lKA6C1ZCLxw2VNlZAEbwX988OjtFnkxrRMW0FXkLFZCLR9mNex8wYxIBBuWUSYYAmnVDK1Os35BGzYFibKqUy9JRdpyIRygbaw8XAnqOOac'

# Inisialisasi layanan YouTube API
instagram = build('instagram', 'v3', developerKey=instagram_api_key)
def search_posts_by_keyword(keyword, max_results=10):
    """
    Cari postingan Instagram berdasarkan kata kunci dalam caption.
    """
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token={ACCESS_TOKEN}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        sys.exit(1)

    posts = response.json().get('data', [])
    filtered_posts = []

    for post in posts:
        caption = post.get('caption', '')
        if keyword.lower() in caption.lower():
            filtered_posts.append({
                'id': post['id'],
                'caption': caption,
                'media_url': post.get('media_url'),
                'timestamp': post.get('timestamp')
            })
        if len(filtered_posts) >= max_results:
            break

    return filtered_posts

def get_post_comments(post_id, max_results=10):
    """
    Ambil komentar untuk sebuah postingan berdasarkan ID postingan.
    """
    url = f"https://graph.instagram.com/{post_id}/comments?fields=id,text,username&access_token={ACCESS_TOKEN}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching comments for post {post_id}: {response.status_code}, {response.text}")
        return []

    comments = response.json().get('data', [])
    return comments[:max_results]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python crawler_instagram.py <keyword> <max_results>")
        sys.exit(1)

    keyword = sys.argv[1]
    max_results = int(sys.argv[2])

    # Pencarian postingan berdasarkan kata kunci
    results = search_posts_by_keyword(keyword, max_results)
    if not results:
        print("Tidak ada postingan yang ditemukan.")
        sys.exit()

    # Output postingan dan komentar
    for index, post in enumerate(results, start=1):
        print(f"\nPost {index}:")
        print(f"Caption: {post['caption']}")
        print(f"Media URL: {post['media_url']}")
        print(f"Timestamp: {post['timestamp']}")

        # Ambil komentar untuk setiap postingan
        comments = get_post_comments(post['id'])
        if comments:
            print("\nComments:")
            for comment in comments:
                print(f"- {comment['username']}: {comment['text']}")
        else:
            print("No comments available.")
