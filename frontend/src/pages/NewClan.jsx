import { useState } from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import axiosInstance from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

const NewClan = () => {
  const [clanName, setClanName] = useState('');
  const [clanDescription, setClanDescription] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleCreateClan = async () => {
    if (!clanName.trim() || !clanDescription.trim()) {
      setErrorMessage('Пожалуйста, заполните все поля.');
      return;
    }

    try {
      const response = await axiosInstance.post(
        '/clans',
        {
          clanname: clanName,
          description: clanDescription,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        },
      );

      if (response.status === 201) {
        navigate('/clanDetail'); // Перенаправляем на страницу деталей клана
      }
    } catch (error) {
      console.error('Ошибка при создании клана:', error);
      setErrorMessage('Не удалось создать клан. Попробуйте позже.');
    }
  };

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
        Создание нового клана
      </Typography>

      <Box sx={{ mt: 4 }}>
        <TextField
          label="Название клана"
          fullWidth
          value={clanName}
          onChange={(e) => setClanName(e.target.value)}
          sx={{ mb: 3 }}
        />
        <TextField
          label="Описание клана"
          fullWidth
          multiline
          rows={4}
          value={clanDescription}
          onChange={(e) => setClanDescription(e.target.value)}
          sx={{ mb: 3 }}
        />

        {errorMessage && <Typography sx={{ color: 'red', mb: 2 }}>{errorMessage}</Typography>}

        <Button
          variant="contained"
          onClick={handleCreateClan}
          sx={{
            background: '#6b705c',
            color: '#fff',
            fontSize: '16px',
            padding: '10px 20px',
          }}>
          Создать клан
        </Button>
      </Box>
    </Container>
  );
};

export default NewClan;
