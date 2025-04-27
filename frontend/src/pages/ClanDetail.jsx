import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Divider,
  Button,
  TextField,
  FormControlLabel,
  Switch,
  List,
  ListItem,
  ListItemText,
  Avatar,
} from '@mui/material';
import axiosInstance from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

const ClanDetail = () => {
  const [clanData, setClanData] = useState(null);
  const [isOwner, setIsOwner] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [clanName, setClanName] = useState('');
  const [clanDescription, setClanDescription] = useState('');
  const [recruiting, setRecruiting] = useState(false);
  const [requests, setRequests] = useState([]); // Заявки на вступление
  const [members, setMembers] = useState([]); // Участники клана
  const [notification, setNotification] = useState('');
  const [clanMembershipId, setClanMembershipId] = useState(null); // ID членства
  const navigate = useNavigate();

  // Загрузка данных о клане
  const fetchClanData = async () => {
    try {
      const response = await axiosInstance.get('/current_user_info', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        const { clan, clan_membership } = response.data;

        if (clan) {
          setClanData(clan);
          setIsOwner(clan.owner_membership_id === clan_membership.id);
          setClanName(clan.clanname);
          setClanDescription(clan.description);
          setRecruiting(clan.recruiting);
          setClanMembershipId(clan_membership.id); // Сохраняем ID членства

          fetchMembers(clan.id); // Загрузка участников клана
          if (clan.owner_membership_id === clan_membership.id) {
            fetchRequests(clan.id); // Загрузка заявок
          }
        } else {
          navigate('/clansList'); // Если клана нет, перенаправляем
        }
      }
    } catch (error) {
      setNotification('Ошибка загрузки данных. Попробуйте позже.');
    }
  };

  // Загрузка участников клана
  const fetchMembers = async (clanId) => {
    try {
      const response = await axiosInstance.get('/extended/clan_memberships', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        const filteredMembers = response.data.filter((member) => member.clan_id === clanId);

        const membersWithDetails = await Promise.all(
          filteredMembers.map(async (member) => {
            const userResponse = await axiosInstance.get(`/users/${member.user_id}`, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            });
            return { ...member, username: userResponse.data.username };
          }),
        );

        setMembers(membersWithDetails);
      }
    } catch (error) {
      setNotification('Ошибка при загрузке участников. Попробуйте позже.');
    }
  };

  // Загрузка заявок на вступление
  const fetchRequests = async (clanId) => {
    try {
      const response = await axiosInstance.get('/extended/clan_requests', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 200) {
        const requestsWithDetails = await Promise.all(
          response.data
            .filter((request) => request.clan_id === clanId)
            .map(async (request) => {
              const userResponse = await axiosInstance.get(`/users/${request.user_id}`, {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
              });
              return { ...request, username: userResponse.data.username };
            }),
        );
        setRequests(requestsWithDetails);
      }
    } catch (error) {
      setNotification('Ошибка при загрузке заявок. Попробуйте позже.');
    }
  };

  // Принятие заявки на вступление
  const handleAcceptRequest = async (userId) => {
    try {
      await axiosInstance.post(
        '/clan_memberships',
        { user_id: userId },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );

      setRequests((prev) => prev.filter((request) => request.user_id !== userId));
      fetchMembers(clanData.id); // Обновляем список участников
    } catch (error) {
      setNotification('Ошибка при добавлении пользователя. Попробуйте позже.');
    }
  };

  // Сохранение изменений данных о клане
  const handleSaveChanges = async () => {
    try {
      await axiosInstance.patch(
        `/clans/${clanData.id}`,
        {
          clanname: clanName,
          recruiting,
          description: clanDescription,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );

      setEditMode(false);
    } catch (error) {
      setNotification('Ошибка при обновлении информации о клане. Попробуйте позже.');
    }
  };

  // Переключение состояния рекрутинга
  const handleToggleRecruiting = async () => {
    try {
      await axiosInstance.patch(
        `/clans/${clanData.id}`,
        { recruiting: !recruiting },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );

      setRecruiting(!recruiting);
    } catch (error) {
      setNotification('Ошибка при изменении состояния рекрутинга. Попробуйте позже.');
    }
  };

  // Удаление клана
  const handleDeleteClan = async () => {
    try {
      await axiosInstance.delete(`/clans/${clanData.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });

      navigate('/clansList');
    } catch (error) {
      setNotification('Ошибка при удалении клана. Попробуйте позже.');
    }
  };

  // Выход из клана
  const handleLeaveClan = async () => {
    try {
      await axiosInstance.delete(`/clan_memberships/${clanMembershipId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      navigate('/clansList');
    } catch (error) {
      setNotification('Ошибка при выходе из клана.');
    }
  };

  // Переход на страницу клановой войны
  const handleStartClanWar = () => {
    navigate('/clanWars');
  };

  useEffect(() => {
    fetchClanData();
  }, []);

  if (!clanData) {
    return (
      <Container>
        <Typography>Загрузка...</Typography>
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
      <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#6b705c' }}>
        {editMode ? 'Редактирование клана' : `Клан: ${clanData.clanname}`}
      </Typography>

      <Divider sx={{ mb: 4, mt: 4 }} />

      {notification && (
        <Box
          sx={{
            mt: 4,
            background: '#fff',
            padding: '10px',
            borderRadius: '8px',
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
            color: '#6b705c',
          }}>
          <Typography>{notification}</Typography>
        </Box>
      )}

      {!editMode ? (
        <>
          <Typography sx={{ mt: 2, mb: 2 }}>{clanData.description}</Typography>
          <Typography>Рекрутинг: {recruiting ? 'Открыт' : 'Закрыт'}</Typography>

          {!isOwner && (
            <Button
              variant="contained"
              sx={{
                mt: 4,
                background: '#6b705c',
                color: '#fff',
              }}
              onClick={handleLeaveClan}>
              Выйти из клана
            </Button>
          )}

          {isOwner && (
            <Box sx={{ mt: 4 }}>
              <FormControlLabel
                control={
                  <Switch checked={recruiting} onChange={handleToggleRecruiting} color="#6b705c" />
                }
                label={recruiting ? 'Закрыть рекрутинг' : 'Открыть рекрутинг'}
              />
              <Button
                variant="contained"
                sx={{
                  mt: 2,
                  mr: 2,
                  background: '#6b705c',
                  color: '#fff',
                }}
                onClick={handleStartClanWar}>
                Начать Клановую войну
              </Button>
              <Button
                variant="contained"
                sx={{
                  mt: 2,
                  mr: 2,
                  background: '#6b705c',
                  color: '#fff',
                }}
                onClick={() => setEditMode(true)}>
                Редактировать
              </Button>

              <Button
                variant="contained"
                sx={{
                  mt: 2,
                  background: '#6b705c',
                  color: '#fff',
                }}
                onClick={handleDeleteClan}>
                Удалить клан
              </Button>
            </Box>
          )}
        </>
      ) : (
        <Box sx={{ mt: 4 }}>
          <TextField
            label="Название клана"
            fullWidth
            value={clanName}
            onChange={(e) => setClanName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Описание клана"
            fullWidth
            multiline
            rows={3}
            value={clanDescription}
            onChange={(e) => setClanDescription(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            sx={{
              mr: 2,
              background: '#6b705c',
              color: '#fff',
            }}
            onClick={handleSaveChanges}>
            Сохранить
          </Button>
          <Button
            variant="contained"
            sx={{
              background: '#6b705c',
              color: '#fff',
            }}
            onClick={() => setEditMode(false)}>
            Отмена
          </Button>
        </Box>
      )}

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" sx={{ color: '#6b705c', mb: 2 }}>
          Участники клана
        </Typography>
        <List>
          {members.map((member) => (
            <ListItem key={member.id}>
              <Avatar sx={{ mr: 2 }}>{member.username.charAt(0)}</Avatar>
              <ListItemText
                primary={member.username}
                secondary={`Присоединился: ${new Date(
                  new Date(member.joined_at).getTime() + 5 * 60 * 60 * 1000,
                ).toLocaleString()}`}
              />
            </ListItem>
          ))}
        </List>
      </Box>

      {isOwner && requests.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" sx={{ color: '#6b705c', mb: 2 }}>
            Заявки на вступление
          </Typography>
          <List>
            {requests.map((request) => (
              <ListItem key={request.id}>
                <Avatar sx={{ mr: 2 }}>{request.username.charAt(0)}</Avatar>
                <ListItemText primary={request.username} />
                <Button
                  variant="contained"
                  sx={{ ml: 2, background: '#6b705c', color: '#fff' }}
                  onClick={() => handleAcceptRequest(request.user_id)}>
                  Принять
                </Button>
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Container>
  );
};

export default ClanDetail;
