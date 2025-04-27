import { useEffect, useState } from 'react';
import { Container, Typography, Button, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';

const MyClan = () => {
  const [isLoading, setIsLoading] = useState(true); // Состояние загрузки
  const [clan, setClan] = useState(null); // Информация о клане
  const [errorMessage, setErrorMessage] = useState(''); // Сообщения об ошибках
  const navigate = useNavigate();

  // Получение информации о пользователе и клане
  const fetchUserInfo = async () => {
    setIsLoading(true);
    try {
      const response = await axiosInstance.get('/current_user_info', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        const { clan } = response.data;

        // Если пользователь состоит в клане
        if (clan) {
          setClan(clan);
          navigate('/clanDetail'); // Переход на страницу с деталями клана
        } else {
          setClan(null); // Устанавливаем, что пользователь не состоит в клане
        }
      }
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
      setErrorMessage('Не удалось загрузить данные. Попробуйте позже.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUserInfo();
  }, []);

  const handleCreateClan = () => {
    navigate('/newClane'); // Переход на страницу создания клана
  };

  const handleJoinClan = () => {
    navigate('/clansList'); // Переход на страницу списка кланов
  };

  if (isLoading) {
    return (
      <Container
        sx={{
          mt: 12,
          textAlign: 'center',
        }}>
        <CircularProgress />
        <Typography sx={{ mt: 2, color: '#6b705c' }}>Загрузка данных...</Typography>
      </Container>
    );
  }

  if (errorMessage) {
    return (
      <Container
        sx={{
          mt: 12,
          textAlign: 'center',
        }}>
        <Typography variant="h5" sx={{ color: 'red' }}>
          {errorMessage}
        </Typography>
      </Container>
    );
  }

  return (
    <Container
      sx={{
        mt: 12,
        background: '#faf5ee',
        padding: '30px',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
      }}>
      <Typography
        variant="h3"
        gutterBottom
        sx={{
          fontWeight: 'bold',
          color: '#6b705c',
        }}>
        Кланы
      </Typography>

      {/* Если пользователь не состоит в клане */}
      <Typography variant="h5" sx={{ mt: 4, color: '#6b705c' }}>
        Вы пока не состоите в клане. Что хотите сделать?
      </Typography>
      <Button
        variant="contained"
        onClick={handleCreateClan}
        sx={{
          mt: 3,
          py: 1.5,
          px: 4,
          fontSize: '16px',
          background: '#6b705c',
          color: '#fff',
          mr: 2,
        }}>
        Создать клан
      </Button>
      <Button
        variant="outlined"
        onClick={handleJoinClan}
        sx={{
          mt: 3,
          py: 1.5,
          px: 4,
          fontSize: '16px',
          color: '#6b705c',
          borderColor: '#6b705c',
        }}>
        Вступить в клан
      </Button>
    </Container>
  );
};

export default MyClan;
