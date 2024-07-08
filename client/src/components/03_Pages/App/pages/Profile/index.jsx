import MenuIcon from '@mui/icons-material/Menu';
import { Box, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';

import ProfileAboutPage from '../ProfileAbout';
import ProfileHelpPage from '../ProfileHelp';

import { SidebarLinksData } from './data/SidebarLinksData';
import { MobMenuWrapper, ProfileContentWrapper, ProfileWrapper, SidebarWrapper } from './styled';

import ProfileSidebar from '@/components/04_Widgets/Navigation/Menus/profileSidebar';
import usePageTitle from '@/hooks/usePageTitle';

const ProfileAppPage = () => {
  usePageTitle('profile');
  const [showHeader, setShowHeader] = useState(false);
  const [isSideOpen, setIsSideOpen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 1000) {
        setShowHeader(true);
      } else {
        setShowHeader(false);
      }
    };

    handleResize();

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => setIsSideOpen((prev) => !prev);

  return (
    <ProfileWrapper>
      <SidebarWrapper isSideOpen={isSideOpen}>
        <ProfileSidebar linksData={SidebarLinksData} onClose={toggleSidebar} />
      </SidebarWrapper>
      <ProfileContentWrapper>
        {showHeader && (
          <MobMenuWrapper>
            <MenuIcon onClick={() => toggleSidebar()} />
            <Typography variant="h5" sx={{ flexGrow: 1, textAlign: 'center' }}>
              QPoll
            </Typography>
            <Box sx={{ width: 48 }}></Box>
          </MobMenuWrapper>
        )}
        <Routes>
          <Route path="/" element={<ProfileAboutPage />} />
          <Route path="/contributors" element={'Contributors'} />
          <Route path="/help" element={<ProfileHelpPage />} />
          <Route path="/statistics" element={'Statistics'} />
        </Routes>
      </ProfileContentWrapper>
    </ProfileWrapper>
  );
};

export default ProfileAppPage;
