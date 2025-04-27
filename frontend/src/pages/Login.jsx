import { useState } from 'react';
import { Box, Button, TextField, Typography, Alert } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // Для отображения ошибок
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setError(null);

      const response = await axiosInstance.post(
        '/jwt',
        new URLSearchParams({
          username,
          password,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        },
      );

      if (response.status === 200) {
        const { access_token } = response.data;
        localStorage.setItem('token', access_token);

        // Отправляем событие, чтобы уведомить другие компоненты
        window.dispatchEvent(new Event('authChanged'));

        navigate('/profile');
      }
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setError('Неверные учетные данные');
      } else {
        setError('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
      }
    }
  };

  return (
    <Box
      sx={{
        maxWidth: '400px',
        margin: '0 auto',
        textAlign: 'center',
        mt: 8,
        background: '#faf5ee',
        padding: '30px',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      }}>
      <Typography
        variant="h4"
        sx={{
          mb: 3,
          fontWeight: 'bold',
          color: '#6b705c',
        }}>
        Войти
      </Typography>

      {/* Поля для ввода имени и пароля */}
      <TextField
        label="Имя"
        fullWidth
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        sx={{
          mb: 2,
          background: '#fff',
          borderRadius: '5px',
        }}
      />
      <TextField
        label="Пароль"
        type="password"
        fullWidth
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        sx={{
          mb: 2,
          background: '#fff',
          borderRadius: '5px',
        }}
      />

      {/* Отображение ошибки */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Button
        variant="contained"
        fullWidth
        onClick={handleLogin}
        sx={{
          background: '#6b705c',
          color: '#fff',
          py: 1.5,
          mb: 3,
        }}>
        Войти
      </Button>

      {/* Ссылка на регистрацию */}
      <Typography
        variant="body1"
        sx={{
          color: '#555',
          mb: 2,
        }}>
        Нет аккаунта?
      </Typography>
      <Button
        component={Link}
        to="/register"
        variant="outlined"
        fullWidth
        sx={{
          color: '#6b705c',
          borderColor: '#6b705c',
          py: 1.5,
        }}>
        Зарегистрироваться
      </Button>
    </Box>
  );
};

export default Login;
