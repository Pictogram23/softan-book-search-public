'use client'

import { Container, IconButton, TextField, Typography } from '@mui/material'
import LoupeIcon from '@mui/icons-material/Loupe'
import SendIcon from '@mui/icons-material/Send'
import ChatHuman from './_components/ChatHuman'
import ChatAI from './_components/ChatAI'
import { useCallback, useEffect, useRef, useState } from 'react'

type Chat = {
  isHuman: boolean
  message: string[]
}

type Book = {
  title: string
  creator: string
  url: string
}

export default function Home() {
  const initChat: Chat = {
    isHuman: false,
    message: ['こんにちは！　お探しの本はどんなお話ですか？'],
  }

  const [chatList, setChatList] = useState<Chat[]>([initChat])
  const [keyword, setKeyword] = useState<string>('')
  const [freeze, setFreeze] = useState<boolean>(false)
  const [status, setStatus] = useState<number>(0)

  const ref = useRef<HTMLDivElement>(null)

  const reset = () => {
    if (freeze == false) {
      resetPost()
      const newChatList = chatList.slice(0, chatList.length)
      newChatList.push(initChat)
      setChatList(newChatList)
      setStatus(0)
    }
  }

  const search = async (keyword: string) => {
    if (keyword != '' && freeze == false) {
      setKeyword('')
      setFreeze(true)
      let newChatList = chatList.slice(0, chatList.length)
      newChatList.push({ isHuman: true, message: [keyword] })
      setChatList(newChatList)
      const message = await keywordPost(keyword)
      setChatList((chatList) => {
        newChatList = chatList.slice(0, chatList.length)
        newChatList.push({ isHuman: false, message: message })
        return newChatList
      })
      setFreeze(false)
    }
  }

  const resetPost = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE_URL + '/reset', {
      method: 'POST',
    })
  }

  const keywordPost = async (keyword: string): Promise<string[]> => {
    const formData = new FormData()
    formData.append('search_word', keyword)
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE_URL + '/search', {
      method: 'POST',
      body: formData,
    })
    const jsoned = await res.json()

    const books: Book[] = []
    jsoned.books.map((book: Book) => {
      books.push(book)
    })

    const suggests: string[] = []
    jsoned.suggest.map((suggest: string) => {
      suggests.push(suggest)
    })

    setStatus(jsoned.status)

    let message1 = ''
    let message2 = ''

    message1 = '以下の文庫が見つかりました\t'
    books.map((book) => {
      message1 += book.title + '\t' + book.creator + '\t' + book.url + '\n'
    })
    if (jsoned.status == 2) {
      message2 = '以下のサジェストを参考にキーワードを追加してください\n'
      suggests.map((suggest) => {
        message2 += suggest + ' '
      })
    }

    return [message1, message2]
  }

  const scrollToBottomOfList = useCallback(() => {
    ref!.current!.scrollIntoView({
      behavior: 'smooth',
      block: 'end',
    })
  }, [ref])

  useEffect(() => {
    scrollToBottomOfList()
  })

  return (
    <main
      onKeyDown={(e) => {
        if (e.key == 'Enter') {
          e.preventDefault()
          search(keyword)
        }
      }}
    >
      {/* タイトルとか */}
      <Container sx={{ textAlign: 'center', paddingTop: '5vh' }}>
        <Typography variant='h3'>そふたん -Book Search-</Typography>
      </Container>

      {/* チャット画面 */}
      <Container
        className='chat-area'
        sx={{
          height: '65vh',
          margin: 'auto',
          overflowY: 'auto',
          textAlign: 'left',
          width: '60vw',
        }}
      >
        {chatList.map((chat, index) => {
          if (chat.isHuman == true) {
            return <ChatHuman key={index} message={chat.message} />
          } else {
            return (
              <ChatAI
                key={index}
                message={chat.message}
                status={status}
                inputKeyword={setKeyword}
              />
            )
          }
        })}
        <div ref={ref} />
      </Container>

      {/* 検索バー */}
      <Container
        sx={{
          textAlign: 'center',
          width: '80vw',
          height: '10vh',
          left: '10vw',
          bottom: 40,
          position: 'fixed',
        }}
      >
        <IconButton onClick={reset} size='large'>
          <LoupeIcon fontSize='inherit' />
        </IconButton>
        <TextField
          sx={{ width: '75%' }}
          value={keyword}
          onChange={(e) => {
            setKeyword(e.target.value)
          }}
          InputProps={{
            endAdornment: (
              <IconButton onClick={() => search(keyword)}>
                <SendIcon />
              </IconButton>
            ),
          }}
        />
      </Container>
    </main>
  )
}
