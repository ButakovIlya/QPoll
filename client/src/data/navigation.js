import DashboardIcon from '@mui/icons-material/Dashboard';
import GroupIcon from '@mui/icons-material/Group';
import HomeIcon from '@mui/icons-material/Home';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';

export const appHeaderData = [
  { caption: 'Ваши опросы', to: '/app', icon: DashboardIcon },
  { caption: 'Общедоступные опросы', to: '/polls', icon: GroupIcon },
];

export const appHeaderMobileData = (onExit) => [
  { caption: 'Ваши опросы', to: '/app', icon: DashboardIcon },
  { caption: 'Общедоступные опросы', to: '/polls', icon: GroupIcon },
  { caption: 'Выйти', to: '/', icon: LogoutIcon, onClick: onExit },
];

export const mainHeaderLinksData = [{ caption: 'Главная', to: '/', icon: HomeIcon }];

export const mobileHeaderLinksData = (isAuthenticated) => [
  { caption: 'Главная', to: '/', icon: HomeIcon },
  isAuthenticated
    ? { caption: 'Дэшборд', to: '/app', icon: DashboardIcon }
    : { caption: 'Войти', to: '/signin', icon: LoginIcon },
];

export const adminPanelSidebarLinks = [
  { id: 1, caption: 'Дэшборд', link: 'main' },
  { id: 2, caption: 'Пользователи', link: 'users' },
  { id: 2, caption: 'Обращения', link: 'support' },
  { id: 3, caption: 'Настройки', link: 'settings' },
];
