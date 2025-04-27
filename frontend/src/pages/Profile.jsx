import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Функция для получения дней с учетом текущего дня
  const getLast7DaysWithLabels = () => {
    const today = new Date();
    const last7Days = [];
    for (let i = 6; i >= 0; i--) {
      const day = new Date(today);
      day.setDate(today.getDate() - i);

      if (i === 0) {
        last7Days.push('Сегодня');
      } else {
        const formattedDate = `${String(day.getDate()).padStart(2, '0')}.${String(
          day.getMonth() + 1,
        ).padStart(2, '0')}.${day.getFullYear()}`;
        last7Days.push(formattedDate);
      }
    }
    return last7Days;
  };

  const last7Days = getLast7DaysWithLabels();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get('/current_user', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (response.status === 200) {
          setUserData(response.data);
        }
      } catch (err) {
        setError('Не удалось загрузить данные пользователя.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const deleteUser = async () => {
    if (!userData) return;

    try {
      await axiosInstance.delete(`/users/${userData.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      // Удаляем токен из localStorage
      localStorage.removeItem('token');

      // Отправляем событие, чтобы уведомить Navbar
      window.dispatchEvent(new Event('authChanged'));

      // Перенаправляем на страницу логина
      navigate('/login');
    } catch (err) {
      console.error('Ошибка при удалении пользователя:', err);
    }
  };

  if (loading) {
    return (
      <Container
        sx={{
          mt: 12,
          textAlign: 'center',
        }}>
        <Typography variant="h5" color="textSecondary">
          Загрузка данных...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container
        sx={{
          mt: 12,
          textAlign: 'center',
        }}>
        <Typography variant="h5" color="error">
          {error}
        </Typography>
      </Container>
    );
  }

  const { username, score, d0, d1, d2, d3, d4, d5, d6 } = userData;
  const weeklyPoints = [d6, d5, d4, d3, d2, d1, d0];

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
        Привет, {username}!
      </Typography>

      <Grid container spacing={4} sx={{ mt: 4 }} justifyContent="center">
        {/* Рейтинг пользователя */}
        <Grid item xs={12} md={4}>
          <Box
            sx={{
              background: 'linear-gradient(135deg, #6b705c, #a4c3b2)',
              padding: '20px',
              borderRadius: '15px',
              boxShadow: '0 6px 15px rgba(0, 0, 0, 0.2)',
              textAlign: 'center',
              color: '#fff',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
            }}>
            <Typography
              variant="h5"
              sx={{
                color: '#fefae0',
                fontWeight: 'bold',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                mb: 2,
              }}>
              Ваш рейтинг
            </Typography>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 'bold',
                color: '#fff',
                textShadow: '2px 2px 5px rgba(0, 0, 0, 0.3)',
              }}>
              {score} баллов
            </Typography>
          </Box>
        </Grid>

        {/* Баллы за последнюю неделю */}
        <Grid item xs={12} md={4}>
          <Box
            sx={{
              background: '#fff',
              padding: '20px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
              height: '100%',
            }}>
            <Typography variant="h5" sx={{ color: '#6b705c', mb: 2 }}>
              Баллы за последние 7 дней
            </Typography>
            <List>
              {weeklyPoints.map((points, index) => (
                <ListItem key={index} sx={{ justifyContent: 'space-between' }}>
                  <ListItemText primary={last7Days[index]} />
                  <Typography variant="body1" sx={{ fontWeight: 'bold', color: '#333' }}>
                    {points} баллов
                  </Typography>
                </ListItem>
              ))}
            </List>
          </Box>
        </Grid>

        {/* Действия */}
        <Grid item xs={12} md={4}>
          <Box
            sx={{
              background: '#fff',
              padding: '20px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
              height: '100%',
            }}>
            <Typography variant="h5" sx={{ color: '#6b705c', mb: 2 }}>
              Действия
            </Typography>
            <Button
              component={Link}
              to="/period"
              variant="contained"
              fullWidth
              sx={{
                background: '#6b705c',
                color: '#fff',
                py: 1.5,
                mb: 2,
              }}>
              Период продуктивности
            </Button>
            <Button
              component={Link}
              to="/duels"
              variant="contained"
              fullWidth
              sx={{
                background: '#6b705c',
                color: '#fff',
                py: 1.5,
                mb: 2,
              }}>
              Начать Дуэль
            </Button>
            <Button
              component={Link}
              to="/myClan"
              variant="contained"
              fullWidth
              sx={{
                background: '#6b705c',
                color: '#fff',
                py: 1.5,
                mb: 2,
              }}>
              Мой Клан
            </Button>
            <Button
              variant="contained"
              fullWidth
              onClick={deleteUser}
              sx={{
                background: '#6b705c',
                color: '#fff',
                py: 1.5,
                mt: 2,
              }}>
              Удалить пользователя
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile;
