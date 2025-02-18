import sys
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

if len(sys.argv) < 2:
    print("No file provided.")
    sys.exit(1)
    
file_path = sys.argv[1]
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        sendKeyword = file.read()
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

sendKeyword = sendKeyword.split("@@")
sendKeyword = list(filter(None, sendKeyword))
sendKeyword = ' '.join(sendKeyword)

# 1. Hashtag processing
# Pattern 1: Single or multiple words with no separator
sendKeyword = re.sub(r'#([a-z]+)', r'\1', sendKeyword)

# Pattern 2: Words separated by underscores
sendKeyword = re.sub(r'#([a-z]+)_(\w+)', lambda m: m.group(1) + ' ' + m.group(2).replace('_', ' '), sendKeyword)

# Pattern 3: Words starting with uppercase letters
sendKeyword = re.sub(r'#([A-Z][a-z]+)+', lambda m: ' '.join(re.findall(r'[A-Z][a-z]+', m.group(0))), sendKeyword)

# 2. Case folding
sendKeyword = sendKeyword.lower()

# 3. Remove mentions
sendKeyword = re.sub(r'@\w+', '', sendKeyword)

# 4. Remove URLs
sendKeyword = re.sub(r'https?://\S+|www\.\S+', '', sendKeyword)

# 5. Remove special characters except hashtags
sendKeyword = re.sub(r'[^a-z0-9\s#]', '', sendKeyword)
# 6. Hapus Karakter yang Tidak Didukung
sendKeyword = re.sub(r'[^\x00-\x7F]+', '', sendKeyword)

stem_Keyword = stemmer.stem(sendKeyword)
stop_Keyword = stopper.remove(stem_Keyword)

print(stop_Keyword)
