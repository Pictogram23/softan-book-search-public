from pyndlsearch.client import SRUClient
from pyndlsearch.cql import CQL
from flask import Flask, request
import requests
from janome.tokenizer import Tokenizer
from collections import Counter
import jaconv
global query_words
query_words = []
#app = Flask(__name__)

def filter_words(wordlist, badwords):
    return [word for word in wordlist if not any(badword in word for badword in badwords)]

def searchword(Searchword):
    global suggest
    suggest = []
    t = Tokenizer()
    wordlist = []
    token = t.tokenize(f"{Searchword}").__next__()
    badword = ["私", "こと", "*", "の", "!", "?", "たち", "&"]  # いらない単語リスト
    badword.append(Searchword)
    badword.append(token.reading)
    badword.append(jaconv.kata2hira(token.reading))
    url = f"https://www.googleapis.com/books/v1/volumes?q={Searchword}&maxResults=20"
    response = requests.get(url)
    data = response.json()
    # 名詞をwordlistに追加
    for item in data.get("items", []):
        title = item["volumeInfo"].get("title", "No title")
        description = item["volumeInfo"].get("description", "No description")
        wordlist.extend([token.surface for token in t.tokenize(description) if token.part_of_speech.startswith('名詞')])
    # badword内の言葉を含む単語をwordlistから取り除く
    filtered_wordlist = filter_words(wordlist, badword)
    word_counts = Counter(filtered_wordlist)
    # 頻出単語の上位30件を表示
    for word, count in word_counts.most_common(5):
        suggest.append(word)
        #print(f"{word}: {count}")

def wakachigaki(s):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
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
            books.append(record_memory)
            record_memory = {}
        status =1
    if int(srres.numberOfRecords) >= 20:
        status =2

def search(s):
    global query_words    
    global status
    global books
    global suggest
    #keywords = query_words.append(request.form.get("search_word"))
    keywords=(" ".join(s))
    searchword(keywords)
    ndlsearch(keywords)
    json={}
    json["status"]=status
    json["books"]=books
    json["suggest"]=suggest
    return json

print(search("猫"))
