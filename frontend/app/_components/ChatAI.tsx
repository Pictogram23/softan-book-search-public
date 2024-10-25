import {
  Box,
  Button,
  Grid,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import SmartToyIcon from '@mui/icons-material/SmartToy'

type Props = {
  message: string[]
  status: number
  inputKeyword: (keyword: string) => void
}

const ChatAI = ({ message, status, inputKeyword }: Props) => {
  let splited: string[] = []
  if (message[1] != undefined) {
    splited = message[1].split('\n')
  }

  let secondary = <></>
  if (splited.length > 1) {
    secondary = (
      <div>
        {splited[1].split(' ').map((m, index) => {
          if (index >= splited[1].split(' ').length - 1) {
            return <></>
          }
          return (
            <Button
              variant='outlined'
              sx={{ marginRight: 1, marginBottom: 1 }}
              key={index}
              onClick={() => inputKeyword(m)}
            >
              {m}
            </Button>
          )
        })}
      </div>
    )
  }

  return (
    <Box>
      <List>
        <ListItem>
          <ListItemIcon>
            <SmartToyIcon />
          </ListItemIcon>
          <ListItemText primary='そふたん' />
        </ListItem>
        {status == 2 ? (
          <>
            <ListItem>
              <ListItemIcon></ListItemIcon>
              <ListItemText sx={{ whiteSpace: 'pre-line' }} secondary={message[0]} />
            </ListItem>
            <ListItem>
              <ListItemIcon></ListItemIcon>
              <ListItemText sx={{ whiteSpace: 'pre-line' }} secondary={splited[0]} />
            </ListItem>
            <ListItem>
              <ListItemIcon></ListItemIcon>
              <div style={{ display: 'flex' }}>{secondary}</div>
            </ListItem>
          </>
        ) : (
          <ListItem>
            <ListItemIcon></ListItemIcon>
            <ListItemText sx={{ whiteSpace: 'pre-line' }} secondary={message[0]} />
          </ListItem>
        )}
      </List>
    </Box>
  )
}
export default ChatAI
