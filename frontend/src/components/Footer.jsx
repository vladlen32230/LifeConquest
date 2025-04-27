import { Box, Typography } from '@mui/material';

const Footer = () => {
  return (
    <Box
      sx={{
        backgroundColor: '#faf5ee',
        color: '#6b705c',
        borderTop: '1px solid #ddd',
        textAlign: 'center',
        padding: '20px 0',
        position: 'relative',
        bottom: 0,
        width: '100%',
        mt: 'auto',
      }}>
      <Typography variant="body2" sx={{ mb: 1 }}>
        © {new Date().getFullYear()} Продуктивность.
      </Typography>
    </Box>
  );
};

export default Footer;
