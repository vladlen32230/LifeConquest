import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token'); // Проверяем токен

  // Если токена нет, перенаправляем на страницу логина
  if (!token) {
    return <Navigate to="/login" />;
  }

  // Если токен есть, рендерим дочерний компонент
  return children;
};

export default PrivateRoute;
