import { Close as CloseIcon } from '@mui/icons-material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import { Box, IconButton, Stack, Tab } from '@mui/material';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { publishPollFx } from './model/publish-poll';
import { MobMenuWrapper, StyledNavContainer, TabsMenu } from './styled';

import FrmShare from '@/components/04_Widgets/Data/Forms/frmShare';
import { StyledNavLink } from '@/components/05_Features/DataDisplay/Out/appHeaderNavOut/styled';
import PollSettingsMenuBtn from '@/components/07_Shared/UIComponents/Buttons/pollSettingsMenuBtn';
import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import { useAlert } from '@/hooks/useAlert';
import usePollData from '@/hooks/usePollData';

const PollSettingsMenuNavigation = ({ buttons }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { pollStatus } = usePollData(id);
  const { showAlert } = useAlert();
  const [isPublished, setIsPublished] = useState(pollStatus);
  const [successOpen, setSuccessOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState(0);
  const [frmShareCapt, setFrmShareCapt] = useState('');
  const [isTabsOpen, setIsTabsOpen] = useState(false);

  useEffect(() => {
    setIsPublished(pollStatus);
  }, [pollStatus]);

  useEffect(() => {
    const currentPath = location.pathname;
    const selectedIndex = buttons.findIndex((button) => currentPath.includes(button.page));
    setSelectedTab(selectedIndex !== -1 ? selectedIndex : 0);
  }, [location, buttons]);

  const handlePublishPoll = async () => {
    const data = await publishPollFx({ id });
    if (data.severity === 'success') {
      setFrmShareCapt('Опрос успешно опубликован !');
      setSuccessOpen(true);
      setIsPublished(true);
    } else {
      showAlert(data.message, data.severity);
    }
  };

  const handleShareOpen = () => {
    setFrmShareCapt('Поделитесь вашим опросом !');
    setSuccessOpen(true);
  };

  return (
    <>
      <StyledNavContainer>
        {window.innerWidth < 1000 ? (
          <MobMenuWrapper>
            <IconButton
              sx={{ display: 'flex', alignItems: 'center', columnGap: '10px' }}
              onClick={() => setIsTabsOpen(!isTabsOpen)}
            >
              {buttons[selectedTab]?.label}
              {!isTabsOpen ? <ArrowDropDownIcon /> : <ArrowDropUpIcon />}
            </IconButton>
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: isTabsOpen ? 'auto' : 0, opacity: isTabsOpen ? 1 : 0 }}
              transition={{ duration: 0.5 }}
              sx={{ overflow: 'hidden' }}
            >
              <TabsMenu onChange={(event, newValue) => setSelectedTab(newValue)}>
                {buttons.map((button, index) => (
                  <StyledNavLink
                    key={button.label}
                    end
                    to={`/app/tests/${id}/${button.page}`}
                    className={({ isActive, isPending }) =>
                      isPending ? 'pending' : isActive ? 'active' : ''
                    }
                    isDisabled={button.disabled}
                    onClick={() => {
                      setSelectedTab(index);
                      setIsTabsOpen(false);
                    }}
                  >
                    <Tab sx={{ width: '100%' }} label={button.label} disabled={button.disabled} />
                  </StyledNavLink>
                ))}
                {!isPublished ? (
                  <Tab key="publish" label="Опубликовать" onClick={() => handlePublishPoll()} />
                ) : (
                  <Tab key="share" label="Поделиться" onClick={() => handleShareOpen()} />
                )}
              </TabsMenu>
            </motion.div>
          </MobMenuWrapper>
        ) : (
          <>
            <Stack direction="row" spacing={2}>
              {buttons.map((button) => (
                <PollSettingsMenuBtn
                  key={button.label}
                  icon={button.icon}
                  label={button.label}
                  page={button.page}
                  disabled={button.disabled}
                />
              ))}
            </Stack>
            <Box sx={{ display: 'flex', alignItems: 'center', columnGap: '10px' }}>
              {!isPublished && (
                <PrimaryButton handleClick={() => handlePublishPoll()} caption="Опубликовать" />
              )}
              {isPublished && (
                <PrimaryButton
                  style={{ alignSelf: 'end' }}
                  caption="Поделиться"
                  handleClick={() => handleShareOpen()}
                />
              )}
              <IconButton onClick={() => navigate(`/app`)}>
                <CloseIcon />
              </IconButton>
            </Box>
          </>
        )}
      </StyledNavContainer>
      <FrmShare open={successOpen} setOpen={setSuccessOpen} caption={frmShareCapt} />
    </>
  );
};

export default PollSettingsMenuNavigation;
