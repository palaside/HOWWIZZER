import { useNavigate } from 'react-router-dom';

export const useAppNavigation = () => {
  const navigate = useNavigate();

  const goToDashboard = () => navigate('/dashboard');
  const goToLogin = () => navigate('/login');
  const goBack = () => navigate(-1);

  return { goToDashboard, goToLogin, goBack };
};
