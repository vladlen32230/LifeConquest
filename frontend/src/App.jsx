import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Period from './pages/Period';
import Duels from './pages/Duels';
import MyClan from './pages/MyClan';
import ClansList from './pages/ClansList';
import Leaderboard from './pages/Leaderboard';
import Register from './pages/Register';
import Login from './pages/Login';
import Profile from './pages/Profile';
import NewClan from './pages/NewClan';
import ClanDetail from './pages/ClanDetail';
import ClanWars from './pages/ClanWars';
import PrivateRoute from './components/PrivateRoute';
import { Box } from '@mui/material';

function App() {
  return (
    <Router>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
        }}>
        <Navbar />
        <Box
          sx={{
            flexGrow: 1,
            padding: '20px',
            background: '#fdfdfb',
          }}>
          <Routes>
            {/* Доступные всем маршруты */}
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />

            {/* Защищённые маршруты */}
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              }
            />
            <Route
              path="/period"
              element={
                <PrivateRoute>
                  <Period />
                </PrivateRoute>
              }
            />
            <Route
              path="/duels"
              element={
                <PrivateRoute>
                  <Duels />
                </PrivateRoute>
              }
            />
            <Route
              path="/myClan"
              element={
                <PrivateRoute>
                  <MyClan />
                </PrivateRoute>
              }
            />
            <Route
              path="/newClane"
              element={
                <PrivateRoute>
                  <NewClan />
                </PrivateRoute>
              }
            />
            <Route
              path="/clanDetail"
              element={
                <PrivateRoute>
                  <ClanDetail />
                </PrivateRoute>
              }
            />
            <Route
              path="/clansList"
              element={
                <PrivateRoute>
                  <ClansList />
                </PrivateRoute>
              }
            />
            <Route
              path="/clanWars"
              element={
                <PrivateRoute>
                  <ClanWars />
                </PrivateRoute>
              }
            />
            <Route
              path="/leaderboard"
              element={
                <PrivateRoute>
                  <Leaderboard />
                </PrivateRoute>
              }
            />
          </Routes>
        </Box>
        <Footer />
      </Box>
    </Router>
  );
}

export default App;
