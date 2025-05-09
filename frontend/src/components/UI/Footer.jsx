import { 
  Box, 
  Container, 
  Typography, 
  Link, 
  Divider, 
  Grid,
  IconButton,
  useTheme
} from '@mui/material';
import { 
  GitHub as GitHubIcon,
  LinkedIn as LinkedInIcon,
  Twitter as TwitterIcon,
  Facebook as FacebookIcon
} from '@mui/icons-material';

function Footer() {
  const theme = useTheme();
  const currentYear = new Date().getFullYear();
  
  const footerLinks = [
    {
      title: 'Product',
      links: [
        { name: 'Features', url: '#' },
        { name: 'Pricing', url: '#' },
        { name: 'FAQ', url: '#' },
      ]
    },
    {
      title: 'Resources',
      links: [
        { name: 'Documentation', url: '#' },
        { name: 'Blog', url: '#' },
        { name: 'Tutorials', url: '#' },
      ]
    },
    {
      title: 'Company',
      links: [
        { name: 'About', url: '#' },
        { name: 'Contact', url: '#' },
        { name: 'Privacy Policy', url: '#' },
      ]
    }
  ];
  
  const socialLinks = [
    { icon: <GitHubIcon />, url: 'https://github.com' },
    { icon: <LinkedInIcon />, url: 'https://linkedin.com' },
    { icon: <TwitterIcon />, url: 'https://twitter.com' },
    { icon: <FacebookIcon />, url: 'https://facebook.com' }
  ];
  
  return (
    <Box 
      component="footer" 
      sx={{ 
        py: 3, 
        mt: 'auto',
        backgroundColor: theme.palette.background.paper,
        borderTop: `1px solid ${theme.palette.divider}`,
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          {footerLinks.map((column, index) => (
            <Grid item xs={12} sm={4} key={index}>
              <Typography variant="h6" color="textPrimary" gutterBottom>
                {column.title}
              </Typography>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {column.links.map((link, linkIndex) => (
                  <li key={linkIndex} style={{ marginBottom: '0.5rem' }}>
                    <Link
                      href={link.url}
                      variant="body2"
                      color="textSecondary"
                      sx={{ textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </Grid>
          ))}
        </Grid>
        
        <Divider sx={{ my: 3 }} />
        
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', sm: 'row' },
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Typography variant="body2" color="textSecondary">
            © {currentYear} Study Assistant. All rights reserved.
          </Typography>
          
          <Box sx={{ display: 'flex', mt: { xs: 2, sm: 0 } }}>
            {socialLinks.map((social, index) => (
              <IconButton
                key={index}
                color="inherit"
                href={social.url}
                target="_blank"
                rel="noopener noreferrer"
                size="small"
                sx={{ ml: 1 }}
              >
                {social.icon}
              </IconButton>
            ))}
          </Box>
        </Box>
      </Container>
    </Box>
  );
}

export default Footer;