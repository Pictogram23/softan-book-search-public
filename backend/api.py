from pyndlsearch.client import SRUClient
from pyndlsearch.cql import CQL
from flask import Flask, request
import requests
from janome.tokenizer import Tokenizer
from collections import Counter
import jaconv
global query_words
query_words = []
app = Flask(__name__)

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

def searchword(Searchword):
    Searchwords = Searchword.replace(' ', '+') 
    global suggest
    suggest = []    
    t = Tokenizer()
    wordlist = []
    token = t.tokenize(f"{Searchword}").__next__()
    badword = [
    "私", "こと", "*", "の", "!", "?", "たち", "&", "さん", "description", "No", 
    "くん", "ちゃん", "ため", "/", "章", "化", "学", "的", "(", ")", "者", ":", "冊", 
    "これ", "それ", "あれ", "この", "その", "あの", "ここ", "そこ", "あそこ", "こちら", 
    "どれ", "何", "どこ", "もの", "ため", "よう", "こと", "人", "ー", "〜", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "〇", "零", "壱", "弐", "参", 
    "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", 
    "@", "#", "$", "%", "^", "&", "*", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ";", "'", "\"", "<", ">", ",", ".", "?", "～", "-"
    ]
    #Badsearchword = Searchword.split()
    for word in Searchwords:
        token = t.tokenize(f"{word}").__next__()
        badword.append(word)
        badword.append(token.reading)
        badword.append(jaconv.kata2hira(token.reading))
    API_KEY = "Secret"

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
            #title = item["volumeInfo"].get("title", "No title")
            description = item["volumeInfo"].get("description", "No description")
            wordlist.extend([token.surface for token in t.tokenize(description) if token.part_of_speech.startswith('名詞')])
        # badword内の言葉を含む単語をwordlistから取り除く
        filtered_wordlist = filter_words(wordlist, badword)
        word_counts = Counter(filtered_wordlist)
        # 頻出単語の上位10件を表示
        for word, count in word_counts.most_common(10):
            suggest.append(word)
            #print(f"{word}: {count}")

def wakachigaki(s):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    #s = "可愛い猫の本"
    input_text = list(t.tokenize(s, wakati=True))
    part_of_speech = []
    for content in input_text:
        token = t.tokenize(content).__next__()
        part_of_speech.append(token.part_of_speech.split(',')[0])
    word_list = []
    count = 0
    for content in part_of_speech:
        if content != "助詞":
            #or content == "形容詞" or content == "副詞":
            word_list.append(input_text[count])
        count += 1
    return word_list

def ndlsearch(keyword):
    global status
    global books
    status = 0
    cql = CQL()
    cql.description = " ".join(keyword)
    client = SRUClient(cql)
    client.set_maximum_records(20)
    srres = client.get_srresponse()
    if srres.numberOfRecords == 0:
        return status
    else:
        books = []
        record_memory = {}
        for record in srres.records:
            record_memory["title"]=record.recordData.title
            record_memory["creator"]=record.recordData.creator
            record_memory["url"]=f"https://ndlsearch.ndl.go.jp/api/openurl?&au={record.recordData.creator}&btitle={record.recordData.title}"
            books.append(record_memory)
            record_memory = {}
        status =1
    if int(srres.numberOfRecords) >= 20:
        status =2

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*') # すべてのオリジンを許可
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') # 使用するヘッダーに応じて追加
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/search",methods=["POST"])
def search():
    global query_words
    global status
    global books
    global suggest
    keywords = query_words.append(request.form.get("search_word"))
    keywords=(" ".join(query_words))
    searchword(keywords)
    ndlsearch(keywords)
    json={}
    json["status"]=status
    json["books"]=books
    json["suggest"]=suggest
    return json

@app.route("/reset",methods=["POST"])
def reset():
    global query_words
    query_words = []
    return {}

if __name__ == '__main__':
    app.run(debug=True)
