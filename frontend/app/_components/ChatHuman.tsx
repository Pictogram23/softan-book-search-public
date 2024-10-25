import { Box, Grid, List, ListItem, ListItemIcon, ListItemText } from '@mui/material'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'

type Props = {
  message: string[]
}

const ChatHuman = ({ message }: Props) => {
  return (
    <Box>
      <List>
        <ListItem>
          <ListItemIcon>
            <AccountCircleIcon />
          </ListItemIcon>
          <ListItemText primary='自分' />
        </ListItem>
        <ListItem>
          <ListItemIcon></ListItemIcon>
          <ListItemText sx={{ whiteSpace: 'pre-line' }} secondary={message[0]} />
        </ListItem>
      </List>
    </Box>
  )
}
export default ChatHuman
