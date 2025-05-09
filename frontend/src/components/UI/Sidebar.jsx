import { 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  Divider, 
  Box, 
  Typography,
  useTheme,
  ListItemButton
} from '@mui/material';
import { 
  Home as HomeIcon, 
  Article as ArticleIcon, 
  Chat as ChatIcon, 
  School as SchoolIcon, 
  Settings as SettingsIcon, 
  HelpOutline as HelpIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

function Sidebar({ open }) {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  
  const mainMenuItems = [
    { text: 'Home', icon: <HomeIcon />, path: '/' },
    { text: 'Documents', icon: <ArticleIcon />, path: '/documents' },
    { text: 'Chat', icon: <ChatIcon />, path: '/chat' },
    { text: 'Study Tools', icon: <SchoolIcon />, path: '/study-tools' },
  ];
  
  const secondaryMenuItems = [
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    { text: 'Help', icon: <HelpIcon />, path: '/help' },
  ];
  
  const isActive = (path) => {
    return location.pathname === path;
  };
  
  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', height: 64 }}>
        <SchoolIcon sx={{ mr: 1, color: theme.palette.primary.main }} />
        <Typography variant="h6" component="div">
          Study AI
        </Typography>
      </Box>
      
      <Divider />
      
      <List>
        {mainMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              onClick={() => navigate(item.path)}
              selected={isActive(item.path)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: theme.palette.primary.light,
                  color: theme.palette.primary.contrastText,
                  '& .MuiListItemIcon-root': {
                    color: theme.palette.primary.contrastText,
                  },
                },
                '&.Mui-selected:hover': {
                  backgroundColor: theme.palette.primary.main,
                },
              }}
            >
              <ListItemIcon sx={{ color: isActive(item.path) ? theme.palette.primary.contrastText : 'inherit' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
      <Box sx={{ flexGrow: 1 }} />
      
      <Divider />
      
      <List>
        {secondaryMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => navigate(item.path)}>
              <ListItemIcon>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}

export default Sidebar;