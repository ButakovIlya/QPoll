import { Box, List, ListItem, ListItemButton, ListItemText, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { NavLink, Route, Routes, useNavigate } from 'react-router-dom';

import AdminSettings from './pages/AdminSettings';
import AdmSupportPage from './pages/AdminSupport';
import AdminUsersPage from './pages/AdminUsers';
import {
  AdmContentWrapper,
  AdmRouterWrapper,
  AdminPanelWrapper,
  StyledDrawerWrapper,
} from './styled';

import { colorConfig } from '@/app/template/config/color.config';
import AdmHeader from '@/components/04_Widgets/Navigation/Menus/admHeader';
import { adminPanelSidebarLinks } from '@/data/navigation';

const AdminPanelPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    navigate('/admin-panel/main');
  }, []);

  return (
    <AdminPanelWrapper>
      <AdmContentWrapper>
        <StyledDrawerWrapper variant="permanent" anchor="left">
          <Typography variant="h6" noWrap component="div" sx={{ p: 2 }}>
            Админ Панель
          </Typography>
          <List>
            {adminPanelSidebarLinks.map(({ caption, link }) => (
              <ListItem key={caption} disablePadding>
                <NavLink
                  to={`/admin-panel/${link}`}
                  style={({ isActive }) => ({
                    textDecoration: 'none',
                    color: isActive ? '#fff' : '#000',
                    backgroundColor: isActive ? colorConfig.primaryBlue : 'transparent',
                    width: '100%',
                  })}
                >
                  <ListItemButton>
                    <ListItemText primary={caption} />
                  </ListItemButton>
                </NavLink>
              </ListItem>
            ))}
            <ListItem key={'Назад'} disablePadding>
              <NavLink
                to={`/app`}
                style={({ isActive }) => ({
                  textDecoration: 'none',
                  color: isActive ? '#fff' : '#000',
                  backgroundColor: isActive ? colorConfig.primaryBlue : 'transparent',
                  width: '100%',
                })}
              >
                <ListItemButton>
                  <ListItemText primary={'Назад'} />
                </ListItemButton>
              </NavLink>
            </ListItem>
          </List>
        </StyledDrawerWrapper>
        <AdmRouterWrapper component="main">
          <AdmHeader />
          <Box sx={{ padding: '20px' }}>
            <Routes>
              <Route
                path="/main"
                element={<Typography paragraph>Это главная страница.</Typography>}
              />
              <Route path="/users" element={<AdminUsersPage />} />
              <Route path="/support" element={<AdmSupportPage />} />
              <Route path="/settings" element={<AdminSettings />} />
            </Routes>
          </Box>
        </AdmRouterWrapper>
      </AdmContentWrapper>
    </AdminPanelWrapper>
  );
};

export default AdminPanelPage;
