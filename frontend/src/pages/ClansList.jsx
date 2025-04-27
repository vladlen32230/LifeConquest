import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Divider,
} from '@mui/material';
import axiosInstance from '../api/axiosInstance';

const ClansList = () => {
  const [clans, setClans] = useState([]); // Список всех кланов
  const [memberships, setMemberships] = useState([]); // Список всех участий в кланах
  const [userClan, setUserClan] = useState(null); // Данные о клане пользователя
  const [isOwner, setIsOwner] = useState(false); // Флаг владельца клана
  const [isLoading, setIsLoading] = useState(true); // Состояние загрузки
  const [statusMessage, setStatusMessage] = useState(''); // Сообщение о статусе
  const [disabledButtons, setDisabledButtons] = useState([]); // Состояние кнопок

  const fetchData = async () => {
    setIsLoading(true);
    try {
      // Запрос на информацию о текущем пользователе
      const userResponse = await axiosInstance.get('/current_user_info', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      let currentUserClan = null;

      if (userResponse.status === 200) {
        const { clan, clan_membership } = userResponse.data;
        setUserClan(clan);
        currentUserClan = clan;

        if (clan && clan.owner_membership_id === clan_membership.id) {
          setIsOwner(true);
        }
      }

      // Запрос на список кланов
      const clansResponse = await axiosInstance.get('/extended/clans', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      // Запрос на список участий в кланах
      const membershipsResponse = await axiosInstance.get('/extended/clan_memberships', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (clansResponse.status === 200 && membershipsResponse.status === 200) {
        const filteredClans = clansResponse.data.filter(
          (clan) => !(currentUserClan && clan.id === currentUserClan.id), // Исключаем клан пользователя
        );
        setClans(filteredClans);
        setMemberships(membershipsResponse.data); // Сохраняем все участия в кланах
      }
    } catch (error) {
      setStatusMessage('Не удалось загрузить данные. Попробуйте позже.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleApply = async (clanId) => {
    setDisabledButtons((prev) => [...prev, clanId]); // Отключаем кнопку
    try {
      await axiosInstance.post(
        '/clan_requests',
        { clan_id: clanId },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );
      setStatusMessage('Заявка успешно отправлена!');
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setStatusMessage('Вы уже отправили запрос в этот клан.');
      } else {
        setStatusMessage('Не удалось отправить заявку. Попробуйте позже.');
      }
    } finally {
      setDisabledButtons((prev) => prev.filter((id) => id !== clanId)); // Включаем кнопку
    }
  };

  const getMembersCount = (clanId) => {
    return memberships.filter((membership) => membership.clan_id === clanId).length;
  };

  return (
    <Container
      sx={{
        mt: 12,
        background: '#faf5ee',
        padding: '30px',
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
        Список кланов
      </Typography>
      <Divider sx={{ mb: 4 }} />

      {statusMessage && (
        <Typography
          align="center"
          sx={{
            mb: 4,
            fontWeight: 'bold',
            color: '#6b705c',
          }}>
          {statusMessage}
        </Typography>
      )}

      {isLoading ? (
        <Typography align="center" sx={{ mt: 3, color: '#6b705c' }}>
          Загрузка...
        </Typography>
      ) : clans.length === 0 ? (
        <Typography align="center" sx={{ mt: 3, color: '#6b705c' }}>
          Нет доступных кланов.
        </Typography>
      ) : (
        <Box sx={{ mt: 4 }}>
          {clans.map((clan) => (
            <Card
              key={clan.id}
              sx={{
                mb: 4,
                background: '#fff',
                borderRadius: '10px',
                boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
                textAlign: 'left',
              }}>
              <CardContent>
                <Typography variant="h5" sx={{ color: '#6b705c', mb: 1 }}>
                  {clan.clanname}
                </Typography>
                <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
                  {clan.description}
                </Typography>
                <Typography variant="body2" sx={{ color: '#333' }}>
                  Количество членов клана: {getMembersCount(clan.id)}
                </Typography>
                <Typography variant="body2" sx={{ color: '#333' }}>
                  Рекрутинг: {clan.recruiting ? 'Открыт' : 'Закрыт'}
                </Typography>
                <Typography variant="body2" sx={{ color: '#333', mt: 1 }}>
                  Создан: {new Date(clan.created_at).toLocaleString()}
                </Typography>
              </CardContent>
              {clan.recruiting && !userClan && (
                <CardActions>
                  <Button
                    variant="contained"
                    sx={{
                      background: '#6b705c',
                      color: '#fff',
                    }}
                    disabled={disabledButtons.includes(clan.id)}
                    onClick={() => handleApply(clan.id)}>
                    Подать заявку
                  </Button>
                </CardActions>
              )}
            </Card>
          ))}
        </Box>
      )}
    </Container>
  );
};

export default ClansList;
