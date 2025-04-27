import { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button, Container, Box, Menu, MenuItem } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Состояние авторизации
  const [anchorEl, setAnchorEl] = useState(null); // Состояние для меню "Войти / Регистрация"
  const [clanMenuAnchorEl, setClanMenuAnchorEl] = useState(null); // Состояние для меню "Кланы"
  const navigate = useNavigate();

  // Проверка токена при загрузке
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);

    // Добавляем обработчик события
    const handleAuthChange = () => {
      const updatedToken = localStorage.getItem('token');
      setIsLoggedIn(!!updatedToken);
    };

    window.addEventListener('authChanged', handleAuthChange);

    // Удаляем обработчик при размонтировании
    return () => {
      window.removeEventListener('authChanged', handleAuthChange);
    };
  }, []);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleClanMenuOpen = (event) => {
    setClanMenuAnchorEl(event.currentTarget);
  };

  const handleClanMenuClose = () => {
    setClanMenuAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('token'); // Удаляем токен
    setIsLoggedIn(false); // Обновляем состояние
    navigate('/login'); // Перенаправляем на страницу входа
  };

  return (
    <AppBar
      position="fixed"
      sx={{
        background: '#faf5ee',
        color: '#333',
        boxShadow: 'none',
        borderBottom: '1px solid #ddd',
      }}>
      <Container>
        <Toolbar
          sx={{
            justifyContent: 'space-between',
          }}>
          {/* Логотип с переходом на главную */}
          <Typography
            variant="h6"
            sx={{
              fontWeight: 'bold',
              color: '#6b705c',
              textDecoration: 'none',
            }}
            component={Link}
            to="/">
            Продуктивность
          </Typography>

          {/* Навигация */}
          <Box>
            <Button component={Link} to="/profile" sx={{ color: '#6b705c', mx: 1 }}>
              Профиль
            </Button>
            <Button component={Link} to="/period" sx={{ color: '#6b705c', mx: 1 }}>
              Периоды
            </Button>
            <Button component={Link} to="/duels" sx={{ color: '#6b705c', mx: 1 }}>
              Дуэли
            </Button>

            {/* Кланы раскрывающееся меню */}
            <Button onClick={handleClanMenuOpen} sx={{ color: '#6b705c', mx: 1 }}>
              Кланы
            </Button>
            <Menu
              anchorEl={clanMenuAnchorEl}
              open={Boolean(clanMenuAnchorEl)}
              onClose={handleClanMenuClose}>
              <MenuItem component={Link} to="/myClan" onClick={handleClanMenuClose}>
                Мой клан
              </MenuItem>
              <MenuItem component={Link} to="/clansList" onClick={handleClanMenuClose}>
                Список кланов
              </MenuItem>
            </Menu>

            <Button component={Link} to="/leaderboard" sx={{ color: '#6b705c', mx: 1 }}>
              Лидеры
            </Button>
          </Box>

          {/* Войти / Регистрация или Выйти */}
          <Box>
            {!isLoggedIn ? (
              <>
                <Button
                  onClick={handleMenuOpen}
                  variant="outlined"
                  sx={{
                    color: '#6b705c',
                    borderColor: '#6b705c',
                  }}>
                  Войти / Регистрация
                </Button>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleMenuClose}
                  sx={{ mt: '40px' }}>
                  <MenuItem component={Link} to="/register" onClick={handleMenuClose}>
                    Регистрация
                  </MenuItem>
                  <MenuItem component={Link} to="/login" onClick={handleMenuClose}>
                    Войти
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Button
                onClick={handleLogout}
                variant="outlined"
                sx={{
                  color: '#6b705c',
                  borderColor: '#6b705c',
                }}>
                Выйти
              </Button>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
