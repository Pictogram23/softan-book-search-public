import requests
from janome.tokenizer import Tokenizer
from collections import Counter
import jaconv

def filter_words(wordlist, badwords):
    filtered_words = []
    for word in wordlist:
        if len(word) > 1:  # 単語の長さが1文字より長いかをチェック
            badword_found = False
            for badword in badwords:
                if badword in word:
                    badword_found = True
                    break  # badwordが見つかったらループを抜ける
            if not badword_found:
                filtered_words.append(word)  # badwordが見つからなかったらfiltered_wordsに追加
    return filtered_words

t = Tokenizer()
wordlist = []
Searchword = input("文字列を入力してください")
Searchwords = Searchword.replace(' ', '+') 
badword = [
    "私", "こと", "*", "の", "!", "?", "たち", "&", "さん", "description", "No", 
    "くん", "ちゃん", "ため", "/", "章", "化", "学", "的", "(", ")", "者", ":", "冊", 
    "これ", "それ", "あれ", "この", "その", "あの", "ここ", "そこ", "あそこ", "こちら", 
    "どれ", "何", "どこ", "もの", "ため", "よう", "こと", "人", "ー", "〜", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "〇", "零", "壱", "弐", "参", 
    "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", 
    "@", "#", "$", "%", "^", "&", "*", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ";", "'", "\"", "<", ">", ",", ".", "?", "～", "-"
]

Badsearchword = Searchword.split()
for word in Searchwords:
    token = t.tokenize(f"{word}").__next__()
    badword.append(word)
    badword.append(token.reading)
    badword.append(jaconv.kata2hira(token.reading))

API_KEY = "AIzaSyAWN5BYjv7FXBlT0BnycEshAUpOGjK3g-o"

url = f"https://www.googleapis.com/books/v1/volumes?q={Searchword}&maxResults=40&key={API_KEY}"

response = requests.get(url)

if response.status_code == 429:
    print("APIクエリの制限に達しました。")
else:
    data = response.json()

    totalItems = data.get("totalItems", "NoItem")
    print(totalItems)
    
    # 名詞をwordlistに追加
    for item in data.get("items", []):
        title = item["volumeInfo"].get("title", "No title")
        description = item["volumeInfo"].get("description", "No description")
        wordlist.extend([token.surface for token in t.tokenize(description) if token.part_of_speech.startswith('名詞')])

    # badword内の言葉を含む単語をwordlistから取り除く
    filtered_wordlist = filter_words(wordlist, badword)

    word_counts = Counter(filtered_wordlist)

    # 頻出単語の上位10件を表示
    for word, count in word_counts.most_common(10):
        print(f"{word}: {count}")
