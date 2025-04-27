import { useState, useEffect } from 'react';
import { Container, Typography, Card, CardContent, Button, Box, Divider } from '@mui/material';
import axiosInstance from '../api/axiosInstance';

const Duels = () => {
  const [duelData, setDuelData] = useState(null); // Данные о текущей дуэли
  const [currentUser, setCurrentUser] = useState(null); // Данные текущего пользователя
  const [opponentName, setOpponentName] = useState(''); // Имя соперника
  const [isLoading, setIsLoading] = useState(true); // Загрузка данных
  const [errorMessage, setErrorMessage] = useState(''); // Сообщения об ошибках
  const [duelStatus, setDuelStatus] = useState(''); // Статус текущей дуэли

  const fetchCurrentUserInfo = async () => {
    setIsLoading(true);
    try {
      const response = await axiosInstance.get('/current_user_info', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (response.status === 200) {
        const { user, duel } = response.data;
        setCurrentUser(user); // Устанавливаем данные текущего пользователя
        setDuelData(duel); // Устанавливаем данные о текущей дуэли
        if (duel) {
          const opponentId = duel.user_1_id === user.id ? duel.user_2_id : duel.user_1_id;
          fetchOpponentName(opponentId); // Получаем имя соперника
        }
      }
    } catch (error) {
      console.error('Ошибка при получении данных пользователя:', error);
      setErrorMessage('Не удалось загрузить данные.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchOpponentName = async (opponentId) => {
    try {
      const response = await axiosInstance.get(`/users/${opponentId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (response.status === 200) {
        setOpponentName(response.data.username); // Устанавливаем имя соперника
      }
    } catch (error) {
      console.error('Ошибка при получении имени соперника:', error);
      setOpponentName('Неизвестный соперник');
    }
  };

  const startDuel = async () => {
    try {
      setErrorMessage('');
      setDuelStatus('');
      const response = await axiosInstance.post(
        '/duels',
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );
      const { duel_started, model } = response.data;

      if (duel_started) {
        setDuelData(model); // Устанавливаем данные о новой дуэли
        setDuelStatus('Дуэль началась!');
        const opponentId = model.user_1_id === currentUser.id ? model.user_2_id : model.user_1_id;
        fetchOpponentName(opponentId); // Получаем имя соперника
      } else {
        setDuelStatus('Система подбирает вам соперника...');
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setDuelStatus('Система подбирает вам соперника...');
      } else {
        console.error('Ошибка при начале дуэли:', error);
        setErrorMessage('Не удалось начать дуэль. Попробуйте позже.');
      }
    }
  };

  useEffect(() => {
    fetchCurrentUserInfo();
  }, []);

  const getUserScore = () => {
    if (!duelData || !currentUser) return null;
    return duelData.user_1_id === currentUser.id ? duelData.user_1_score : duelData.user_2_score;
  };

  const getOpponentScore = () => {
    if (!duelData || !currentUser) return null;
    return duelData.user_1_id !== currentUser.id ? duelData.user_1_score : duelData.user_2_score;
  };

  const getEndDate = () => {
    if (!duelData) return null;
    const startDate = new Date(duelData.started_at);
    // Добавляем 3 дня и 5 часов к дате начала
    return new Date(startDate.getTime() + (3 * 24 * 60 * 60 + 5 * 60 * 60) * 1000).toLocaleString();
  };

  return (
    <Container
      sx={{
        mt: 12,
        background: '#faf5ee',
        padding: '40px',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      }}>
      <Typography
        variant="h3"
        gutterBottom
        align="center"
        sx={{
          fontWeight: 'bold',
          color: '#6b705c',
        }}>
        Дуэли
      </Typography>

      <Divider sx={{ mb: 4 }} />
      <Box
        sx={{
          background: '#fff',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          textAlign: 'left',
          mb: 4,
        }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#6b705c' }}>
          Как проходят дуэли?
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Дуэль — это трёхдневное соревнование между двумя участниками. В течение этого времени
          каждый зарабатывает баллы, выполняя продуктивные периоды.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Побеждает тот, кто наберёт больше баллов к концу дуэли. Разница в баллах идёт в качестве
          награды для победителя и штрафа для проигравшего.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Соревнуйтесь и поднимайте свой рейтинг!
        </Typography>
      </Box>
      <Divider sx={{ mb: 4 }} />

      {isLoading ? (
        <Typography align="center" sx={{ color: '#6b705c', mt: 3 }}>
          Загрузка данных...
        </Typography>
      ) : duelData ? (
        <Card
          sx={{
            mt: 3,
            background: '#dcd7c9',
            textAlign: 'center',
            borderRadius: '10px',
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Текущая дуэль
            </Typography>
            <Typography>Ваши баллы: {getUserScore()}</Typography>
            <Typography>Баллы противника: {getOpponentScore()}</Typography>
            <Typography>Соперник: {opponentName}</Typography>
            <Typography>Дуэль заканчивается: {getEndDate()}</Typography>
          </CardContent>
        </Card>
      ) : (
        <Typography align="center" sx={{ color: '#6b705c', mt: 3 }}>
          У вас нет активных дуэлей. Начните новую, чтобы бросить вызов другим пользователям!
        </Typography>
      )}

      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Button
          variant="contained"
          onClick={startDuel}
          disabled={Boolean(duelData)}
          sx={{
            py: 2,
            px: 4,
            fontSize: '16px',
            background: duelData ? '#aaa' : '#6b705c',
          }}>
          Начать дуэль
        </Button>
      </Box>

      {duelStatus && (
        <Typography
          align="center"
          sx={{
            mt: 3,
            fontWeight: 'bold',
            color: '#6b705c',
          }}>
          {duelStatus}
        </Typography>
      )}

      {errorMessage && (
        <Typography
          align="center"
          sx={{
            mt: 3,
            color: 'red',
          }}>
          {errorMessage}
        </Typography>
      )}
    </Container>
  );
};

export default Duels;
