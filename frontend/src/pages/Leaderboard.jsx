import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Card,
  CardContent,
  Avatar,
  Box,
  Button,
  Collapse,
} from '@mui/material';
import axiosInstance from '../api/axiosInstance';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

const Leaderboard = () => {
  const [users, setUsers] = useState([]);
  const [showMore, setShowMore] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axiosInstance.get('/extended/users');
        if (response.status === 200) {
          const sortedUsers = response.data.sort((a, b) => b.score - a.score);
          setUsers(sortedUsers);
        }
      } catch (err) {
        setError('Не удалось загрузить таблицу лидеров.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <Container
        sx={{
          mt: 12,
          textAlign: 'center',
        }}>
        <Typography variant="h5" color="textSecondary">
          Загрузка таблицы лидеров...
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

  const topThreeUsers = users.slice(0, 3);
  const remainingUsers = users.slice(3);

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
        Таблица лидеров
      </Typography>

      <Card
        sx={{
          mt: 4,
          background: '#fff',
          borderRadius: '10px',
          boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          padding: '20px',
        }}>
        <CardContent>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell
                  sx={{
                    fontWeight: 'bold',
                    color: '#6b705c',
                    fontSize: '16px',
                    textAlign: 'center',
                  }}>
                  Место
                </TableCell>
                <TableCell
                  sx={{
                    fontWeight: 'bold',
                    color: '#6b705c',
                    fontSize: '16px',
                  }}>
                  Имя
                </TableCell>
                <TableCell
                  sx={{
                    fontWeight: 'bold',
                    color: '#6b705c',
                    fontSize: '16px',
                    textAlign: 'center',
                  }}>
                  Баллы
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topThreeUsers.map((user, index) => (
                <TableRow
                  key={user.id}
                  sx={{
                    backgroundColor: index === 0 ? '#d4edda' : 'inherit',
                    '&:nth-of-type(odd)': { backgroundColor: '#f9f9f9' },
                  }}>
                  <TableCell
                    sx={{
                      fontWeight: 'bold',
                      color: index === 0 ? '#155724' : '#333',
                      textAlign: 'center',
                    }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {index + 1}
                      {index === 0 && <EmojiEventsIcon sx={{ color: '#FFD700', ml: 1 }} />}
                      {index === 1 && <EmojiEventsIcon sx={{ color: '#C0C0C0', ml: 1 }} />}
                      {index === 2 && <EmojiEventsIcon sx={{ color: '#CD7F32', ml: 1 }} />}
                    </Box>
                  </TableCell>
                  <TableCell
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                    }}>
                    <Avatar
                      sx={{
                        mr: 2,
                        background: '#6b705c',
                        color: '#fff',
                      }}>
                      {user.username.charAt(0)}
                    </Avatar>
                    {user.username}
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 'bold',
                      color: index === 0 ? '#155724' : '#333',
                      textAlign: 'center',
                    }}>
                    {user.score}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {/* Раскрывающееся меню для остальных пользователей */}
          {remainingUsers.length > 0 && (
            <>
              <Box sx={{ textAlign: 'center', mt: 2, mb: 3 }}>
                <Button
                  variant="outlined"
                  onClick={() => setShowMore(!showMore)}
                  sx={{
                    color: '#6b705c',
                    borderColor: '#6b705c',
                    padding: '10px 20px',
                  }}>
                  {showMore ? 'Скрыть остальных' : 'Показать остальных'}
                </Button>
              </Box>
              <Collapse in={showMore}>
                <Table>
                  <TableBody>
                    {remainingUsers.map((user, index) => (
                      <TableRow
                        key={user.id}
                        sx={{
                          '&:nth-of-type(odd)': { backgroundColor: '#f9f9f9' },
                        }}>
                        <TableCell
                          sx={{
                            textAlign: 'center',
                            fontWeight: 'normal',
                          }}>
                          {index + 4}
                        </TableCell>
                        <TableCell
                          sx={{
                            display: 'flex',
                            alignItems: 'center',
                          }}>
                          <Avatar
                            sx={{
                              mr: 2,
                              background: '#6b705c',
                              color: '#fff',
                            }}>
                            {user.username.charAt(0)}
                          </Avatar>
                          {user.username}
                        </TableCell>
                        <TableCell
                          sx={{
                            textAlign: 'center',
                            fontWeight: 'normal',
                          }}>
                          {user.score}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Collapse>
            </>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

export default Leaderboard;
