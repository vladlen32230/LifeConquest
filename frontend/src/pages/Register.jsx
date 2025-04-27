import { useState } from 'react';
import { Box, Button, TextField, Typography, Alert } from '@mui/material';
import axiosInstance from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // Для хранения сообщения об ошибке
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      // Очистка ошибки перед новым запросом
      setError(null);

      // Отправка запроса на сервер
      const response = await axiosInstance.post('/users', {
        username,
        password,
      });

      if (response.status === 201) {
        // Перенаправление на страницу входа
        navigate('/login');
      }
    } catch (err) {
      if (err.response && err.response.status === 409) {
        setError('Имя пользователя не уникальное');
      } else {
        setError('Произошла ошибка. Попробуйте снова.');
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
        Регистрация
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

      {/* Отображение ошибки, если есть */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Button
        variant="contained"
        fullWidth
        onClick={handleRegister}
        sx={{
          background: '#6b705c',
          color: '#fff',
          py: 1.5,
          mt: 2,
        }}>
        Зарегистрироваться
      </Button>
    </Box>
  );
};

export default Register;
