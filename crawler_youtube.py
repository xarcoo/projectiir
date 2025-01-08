from googleapiclient.discovery import build
import sys

# Masukkan API key YouTube Anda di sini
youtube_api_key = 'AIzaSyBydVNxq8ra5s47JqY3zikurqKxkayB9Bg'

# Inisialisasi layanan YouTube API
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def search_videos(query, max_results=5):
    """Mencari video berdasarkan kata kunci."""
    response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='video'
    ).execute()

    videos = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        videos.append({
            'video_id': video_id,
            'title': title,
            'description': description
        })
    return videos

def get_video_comments(video_id, max_results=10):
    """Mengambil komentar untuk video tertentu."""
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results,
        textFormat='plainText'
    ).execute()

    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comments.append({'author': author, 'comment': comment})
    return comments

if __name__ == '__main__':
    # Pastikan ada dua argumen: kata kunci dan jumlah hasil
    if len(sys.argv) < 3:
        print("Usage: python youtube_crawl.py <keyword> <max_results>")
        sys.exit(1)

    keyword = sys.argv[1]
    max_results = int(sys.argv[2])

    # Pencarian video
    videos = search_videos(keyword, max_results)
    if not videos:
        print("Tidak ada video yang ditemukan.")
        sys.exit()

    # Output hasil pencarian video dan komentar
    for index, video in enumerate(videos, start=1):
        # print(f"\nVideo {index}:")
        # print(f"Judul: {video['title']}")
        print(f"{video['description']}")
        # print(f"ID Video: {video['video_id']}")

        # Ambil komentar untuk setiap video
        # comments = get_video_comments(video['video_id'])
        # print("\nKomentar:")
        # for comment in comments:
        #     print(f"- {comment['author']}: {comment['comment']}")
