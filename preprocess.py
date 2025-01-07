import sys
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Initialize stemmer and stopword remover
stemmer = StemmerFactory().create_stemmer()
stopper = StopWordRemoverFactory().create_stop_word_remover()

# Retrieve input text
sendKeyword = sys.argv[1]
sendKeyword = sendKeyword.split("@@")
sendKeyword = list(filter(None, sendKeyword))
sendKeyword = ' '.join(sendKeyword)

# 1. Case folding
sendKeyword = sendKeyword.lower()

# 2. Remove mentions
sendKeyword = re.sub(r'@\w+', '', sendKeyword)

# 3. Remove URLs
sendKeyword = re.sub(r'https?://\S+|www\.\S+', '', sendKeyword)

# 4. Remove special characters except hashtags
sendKeyword = re.sub(r'[^a-z0-9\s#]', '', sendKeyword)

# 5. Hashtag processing
# Pattern 1: Single or multiple words with no separator
sendKeyword = re.sub(r'#([a-z]+)', r'\1', sendKeyword)

# Pattern 2: Words separated by underscores
sendKeyword = re.sub(r'#([a-z]+)_(\w+)', lambda m: m.group(1) + ' ' + m.group(2).replace('_', ' '), sendKeyword)

# Pattern 3: Words starting with uppercase letters
sendKeyword = re.sub(r'#([A-Z][a-z]+)+', lambda m: ' '.join(re.findall(r'[A-Z][a-z]+', m.group(0))), sendKeyword)

stem_Keyword = stemmer.stem(sendKeyword)
stop_Keyword = stopper.remove(stem_Keyword)

print(stop_Keyword)
