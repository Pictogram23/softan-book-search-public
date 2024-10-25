# softan-book-search
自然言語の文章から要求に合致する内容を含む文庫を検索するアプリケーション

## 必要なアプリケーション
- Docker

## 起動方法
`docker-compose up -d`

ログを見たい場合は
`docker-compose up`

## 通信
frontend(ブラウザなどでアクセス)
`http://localhost:3000`

backend(curlコマンドなどでアクセス)
`http://localhost:5000`

## 終了
`docker-compose down`