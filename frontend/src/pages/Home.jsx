import { Container, Typography, Grid, Box } from '@mui/material';

const Home = () => {
  return (
    <Container
      sx={{
        mt: 12,
        background: '#faf5ee',
        padding: '40px',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      }}>
      {/* Приветствие */}
      <Typography
        variant="h3"
        gutterBottom
        align="center"
        sx={{
          fontWeight: 'bold',
          color: '#6b705c',
        }}>
        Добро пожаловать в Продуктивность!
      </Typography>
      <Typography
        variant="h6"
        align="center"
        sx={{
          mb: 6,
          color: '#8a8564',
        }}>
        Соревнуйся, побеждай прокрастинацию и становись лучшей версией себя!
      </Typography>

      {/* Основные возможности */}
      <Grid container spacing={6}>
        <Grid item xs={12} md={6}>
          <Box
            sx={{
              background: '#fff',
              padding: '30px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
            }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: '#6b705c' }}>
              Периоды продуктивности
            </Typography>
            <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
              Установи таймер, сосредоточься на своей работе и получай баллы за выполненные периоды.
              Поднимай свой рейтинг !
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box
            sx={{
              background: '#fff',
              padding: '30px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
            }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: '#6b705c' }}>
              Дуэли
            </Typography>
            <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
              Соревнуйся с другими пользователями. Покажи свою продуктивность !
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box
            sx={{
              background: '#fff',
              padding: '30px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
            }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: '#6b705c' }}>
              Кланы
            </Typography>
            <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
              Создавай кланы, объединяйся с единомышленниками и участвуй в клановых войнах, чтобы
              увеличить свои баллы. Поднимай свой рейтинг !
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box
            sx={{
              background: '#fff',
              padding: '30px',
              borderRadius: '10px',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
            }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: '#6b705c' }}>
              Таблица лидеров
            </Typography>
            <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
              Следи за своими результатами и сравнивай их с другими. Стань лучшим в продуктивности !
            </Typography>
          </Box>
        </Grid>
      </Grid>

      {/* Завершающий блок */}
      <Box
        sx={{
          mt: 6,
          padding: '20px',
          textAlign: 'center',
          background: '#eae7dc',
          borderRadius: '10px',
        }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: '#6b705c' }}>
          Начни свой путь к продуктивности уже сегодня!
        </Typography>
        <Typography variant="body1" sx={{ color: '#555', mb: 2 }}>
          Зарегистрируйся и начни побеждать свою прокрастинацию.
        </Typography>
      </Box>
    </Container>
  );
};

export default Home;
