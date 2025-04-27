import { useState, useEffect, useRef } from 'react';
import { Container, Typography, Box, Slider, Button, Divider } from '@mui/material';

const Period = () => {
  const [cycleTime, setCycleTime] = useState(25); // Время цикла (в минутах)
  const [timeLeft, setTimeLeft] = useState(null); // Оставшееся время (в секундах)
  const [isTimerRunning, setIsTimerRunning] = useState(false); // Состояние таймера
  const [earnedPoints, setEarnedPoints] = useState(null); // Заработанные баллы
  const [successMessage, setSuccessMessage] = useState(null); // Сообщение о начислении баллов
  const [errorMessage, setErrorMessage] = useState(null); // Сообщение об ошибке
  const websocketRef = useRef(null); // Храним WebSocket соединение
  const pageActiveRef = useRef(true); // Флаг активности страницы (используем ref для синхронизации)

  const handleCycleTimeChange = (event, newValue) => {
    if (!isTimerRunning) setCycleTime(newValue);
  };

  const startTimer = () => {
    const jwtToken = localStorage.getItem('token'); // Получаем токен из localStorage
    if (!jwtToken) {
      setErrorMessage('Авторизуйтесь, чтобы начать период продуктивности.');
      return;
    }

    // const ws = new WebSocket(`ws://localhost:8000/task?jwt=${jwtToken}&time=${cycleTime}`);
    // websocketRef.current = ws;

    const ws = new WebSocket(`wss://lifeconquest.ru/api/v1/task?jwt=${jwtToken}&time=${cycleTime}`);
    websocketRef.current = ws;

    ws.onopen = () => {
      setTimeLeft(cycleTime * 60);
      setIsTimerRunning(true);
      setErrorMessage(null);
      setSuccessMessage(null);
      pageActiveRef.current = true; // Устанавливаем флаг активности
    };

    ws.onmessage = (event) => {
      console.log('Сообщение от сервера:', event.data);
    };

    ws.onclose = (event) => {
      if (event.code === 1000 && pageActiveRef.current) {
        setEarnedPoints(cycleTime);
        setSuccessMessage(`Поздравляем! Вы заработали ${cycleTime} баллов.`);
        setTimeout(() => setSuccessMessage(null), 5000);
      } else if (event.code === 3003) {
        setErrorMessage('Время для нового периода ещё не обновилось.');
      } else if (event.code !== 1000) {
        setErrorMessage('Произошла ошибка. Попробуйте снова.');
      }
      setIsTimerRunning(false);
      setTimeLeft(null);
    };

    ws.onerror = () => {
      setErrorMessage('Ошибка подключения к серверу.');
      setIsTimerRunning(false);
    };
  };

  useEffect(() => {
    let timer = null;
    if (isTimerRunning && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      websocketRef.current?.close(1000, 'Таймер завершён');
      setIsTimerRunning(false);
    }
    return () => clearInterval(timer);
  }, [isTimerRunning, timeLeft]);

  // Закрываем WebSocket и обновляем флаг активности при покидании страницы
  useEffect(() => {
    const handleBeforeUnload = () => {
      pageActiveRef.current = false; // Устанавливаем, что пользователь покинул страницу
      if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
        websocketRef.current.close(1000, 'Пользователь покинул страницу');
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
        websocketRef.current.close(1000, 'Компонент размонтирован');
      }
    };
  }, []);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
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
        Период продуктивности
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
          Как это работает?
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Период продуктивности — это время, которое вы посвящаете выполнению своих задач с
          максимальной концентрацией.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Если вы останетесь на сайте до окончания выбранного периода, вам будут начислены баллы,
          равные длительности таймера.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Если же вы покинете страницу до того как таймер закончится, баллы начислены не будут, и вы
          не сможете начать новый период до завершения текущего.
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, color: '#555' }}>
          Если за сутки ни один цикл продуктивности не завершен успешно (пользователь прерывал их),
          рейтинг уменьшается на 30 баллов.
        </Typography>
      </Box>
      <Divider sx={{ mb: 4 }} />

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" sx={{ color: '#6b705c', mb: 2 }}>
          Выберите время для периода продуктивности (минуты)
        </Typography>
        <Slider
          value={cycleTime}
          onChange={handleCycleTimeChange}
          step={5}
          marks
          min={10}
          max={60}
          valueLabelDisplay="auto"
          sx={{
            color: '#6b705c',
            maxWidth: '400px',
            margin: '0 auto',
          }}
        />
        <Typography variant="h6" sx={{ mt: 2, color: '#6b705c' }}>
          Текущее время: {cycleTime} минут
        </Typography>
      </Box>

      {successMessage && (
        <Box sx={{ mt: 4 }}>
          <Typography
            variant="body1"
            sx={{
              color: '#6b705c',
              fontWeight: 'bold',
              textAlign: 'center',
              mt: 2,
            }}>
            {successMessage}
          </Typography>
        </Box>
      )}

      {errorMessage && (
        <Box sx={{ mt: 4 }}>
          <Typography
            variant="body1"
            sx={{
              color: '#6b705c',
              fontWeight: 'bold',
              textAlign: 'center',
              mt: 2,
            }}>
            {errorMessage}
          </Typography>
        </Box>
      )}

      <Box sx={{ mt: 6 }}>
        {timeLeft !== null && (
          <Typography variant="h4" sx={{ color: '#6b705c', mb: 2 }}>
            Оставшееся время: {formatTime(timeLeft)}
          </Typography>
        )}
        <Button
          variant="contained"
          onClick={startTimer}
          disabled={isTimerRunning}
          sx={{
            background: '#6b705c',
            color: '#fff',
            fontSize: '16px',
            padding: '10px 20px',
            mt: 2,
          }}>
          {isTimerRunning ? 'Период запущен' : 'Запустить период'}
        </Button>
      </Box>
    </Container>
  );
};

export default Period;
