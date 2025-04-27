import { useState, useEffect } from 'react';
import { Container, Typography, Card, CardContent, Button, Box, Divider } from '@mui/material';
import axiosInstance from '../api/axiosInstance';

const ClanWars = () => {
  const [warData, setWarData] = useState(null); // Данные о текущей клановой войне
  const [currentClan, setCurrentClan] = useState(null); // Данные текущего клана
  const [opponentClanName, setOpponentClanName] = useState(''); // Имя клана соперника
  const [isLoading, setIsLoading] = useState(true); // Загрузка данных
  const [errorMessage, setErrorMessage] = useState(''); // Сообщения об ошибках
  const [warStatus, setWarStatus] = useState(''); // Статус текущей клановой войны
  const [myClanScore, setMyClanScore] = useState(0); // Суммарные баллы вашего клана
  const [opponentClanScore, setOpponentClanScore] = useState(0); // Суммарные баллы клана соперника

  const fetchCurrentClanInfo = async () => {
    setIsLoading(true);
    try {
      const response = await axiosInstance.get('/current_user_info', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (response.status === 200) {
        const { clan, clan_war } = response.data;
        setCurrentClan(clan); // Устанавливаем данные текущего клана
        setWarData(clan_war); // Устанавливаем данные о текущей войне
        if (clan_war) {
          const opponentClanId =
            clan_war.clan_1_id === clan.id ? clan_war.clan_2_id : clan_war.clan_1_id;
          fetchOpponentClanName(opponentClanId); // Получаем имя клана соперника
          fetchClanScores(clan.id, opponentClanId); // Считаем баллы кланов
        }
      }
    } catch (error) {
      console.error('Ошибка при получении данных клана:', error);
      setErrorMessage('Не удалось загрузить данные.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchOpponentClanName = async (opponentClanId) => {
    try {
      const response = await axiosInstance.get(`/clans/${opponentClanId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (response.status === 200) {
        setOpponentClanName(response.data.clanname); // Устанавливаем имя клана соперника
      }
    } catch (error) {
      console.error('Ошибка при получении имени клана соперника:', error);
      setOpponentClanName('Неизвестный клан');
    }
  };

  const fetchClanScores = async (myClanId, opponentClanId) => {
    try {
      const response = await axiosInstance.get('/extended/clan_war_participants', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        const participants = response.data;

        // Суммируем баллы для текущего клана
        const myScore = participants
          .filter((participant) => participant.clan_id === myClanId)
          .reduce((sum, participant) => sum + participant.score, 0);

        // Суммируем баллы для клана соперника
        const opponentScore = participants
          .filter((participant) => participant.clan_id === opponentClanId)
          .reduce((sum, participant) => sum + participant.score, 0);

        setMyClanScore(myScore);
        setOpponentClanScore(opponentScore);
      }
    } catch (error) {
      console.error('Ошибка при получении баллов кланов:', error);
      setErrorMessage('Не удалось загрузить баллы кланов.');
    }
  };

  const startWar = async () => {
    try {
      setErrorMessage('');
      setWarStatus('');
      const response = await axiosInstance.post(
        '/clan_wars',
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );
      const { clan_war_started, model } = response.data;

      if (clan_war_started) {
        setWarData(model); // Устанавливаем данные о новой войне
        setWarStatus('Клановая война началась!');
        const opponentClanId =
          model.clan_1_id === currentClan.id ? model.clan_2_id : model.clan_1_id;
        fetchOpponentClanName(opponentClanId); // Получаем имя клана соперника
        fetchClanScores(currentClan.id, opponentClanId); // Считаем баллы кланов
      } else {
        setWarStatus('Система подбирает соперника для вашего клана...');
      }
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setWarStatus('Система подбирает соперника для вашего клана...');
      } else {
        console.error('Ошибка при начале клановой войны:', error);
        setErrorMessage('Не удалось начать клановую войну. Попробуйте позже.');
      }
    }
  };

  useEffect(() => {
    fetchCurrentClanInfo();
  }, []);

  const getEndDate = () => {
    if (!warData) return null;
    const startDate = new Date(warData.started_at);
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
        Клановые Войны
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
          Как проходят клановые войны?
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Клановая война — это трёхдневное соревнование, в котором два клана сражаются за
          продуктивность.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Итоговый счёт зависит от суммы баллов всех участников команды, и победит клан, набравший
          больше. Для честной конкуренции в войне участвуют только кланы с равным количеством
          участников.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Разница в баллах идёт в качестве награды для участников клана победителя и штрафа для
          участников проигравшего.
        </Typography>
      </Box>

      {isLoading ? (
        <Typography align="center" sx={{ color: '#6b705c', mt: 3 }}>
          Загрузка данных...
        </Typography>
      ) : warData ? (
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
              Текущая Клановая Война
            </Typography>
            <Typography>Клан соперника: {opponentClanName}</Typography>
            <Typography>Баллы вашего клана: {myClanScore}</Typography>
            <Typography>Баллы клана соперника: {opponentClanScore}</Typography>
            <Typography>Война заканчивается: {getEndDate()}</Typography>
          </CardContent>
        </Card>
      ) : (
        <Typography align="center" sx={{ color: '#6b705c', mt: 3 }}>
          У вашего клана нет активных войн. Начните новую, чтобы бросить вызов другим кланам!
        </Typography>
      )}

      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Button
          variant="contained"
          onClick={startWar}
          disabled={Boolean(warData)}
          sx={{
            py: 2,
            px: 4,
            fontSize: '16px',
            background: warData ? '#aaa' : '#6b705c',
          }}>
          Начать Клановую Войну
        </Button>
      </Box>

      {warStatus && (
        <Typography
          align="center"
          sx={{
            mt: 3,
            fontWeight: 'bold',
            color: '#6b705c',
          }}>
          {warStatus}
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

export default ClanWars;
