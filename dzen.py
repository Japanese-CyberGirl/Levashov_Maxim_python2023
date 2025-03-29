from collections import Counter
from string import punctuation

def count_words(file_path: str):
    cnt = Counter()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = ''.join(ch for ch in line if ch not in punctuation)
            words = line.split()
            cnt.update(words)
    return cnt.most_common(10)

file_path = r"dzen"
res = count_words(file_path)
print(res)