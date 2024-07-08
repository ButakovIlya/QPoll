import InboxIcon from '@mui/icons-material/Inbox';
import { CircularProgress } from '@mui/material';
import { useUnit } from 'effector-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { getAllPoles } from './api/apiRequests';
import {
  ContentWrapper,
  PollsGrid,
  PollsGridWrapper,
  StyledAppContentWrapper,
  StyledArchiveLink,
} from './styled';

import { $polls, setPollsData } from '@/api/store/polls';
import AppPollFilters from '@/components/04_Widgets/Content/Interactive/appPollFilter';
import AppPoleCard from '@/components/04_Widgets/Data/Cards/appPoleCard';
import FrmCreatePoll from '@/components/04_Widgets/Utilities/Modals/frmCreatePoll';
import AppCreateFirstPoll from '@/components/05_Features/UIComponents/Utils/appCreateFirstPoll';
import CustomPagination from '@/components/07_Shared/UIComponents/Navigation/pagination';
import { surveySettings } from '@/data/fields';
import usePageTitle from '@/hooks/usePageTitle';
import usePagination from '@/hooks/usePagination';

const AppPage = () => {
  usePageTitle('app');
  const [$pollsData] = useUnit([$polls, setPollsData]);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState();
  const [loading, setLoading] = useState(true);
  const { pageSize, currPage, totalPages, setTotalPages, handlePageSizeChange, handlePageChange } =
    usePagination();

  const shouldRenderCreateFirstPoll = $pollsData && $pollsData.length === 0;

  const fetchData = async () => {
    const pollResponse = await getAllPoles({ currPage, pageSize });
    setPollsData(pollResponse.results);
    setTotalPages(pollResponse.total_pages);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, [currPage, pageSize]);

  const renderAppContent = () => {
    return shouldRenderCreateFirstPoll ? (
      <AppCreateFirstPoll
        settings={surveySettings}
        handleOpenCreatePoleModal={setIsCreateModalOpen}
      />
    ) : (
      <StyledAppContentWrapper>
        <ContentWrapper>
          <StyledArchiveLink to={'/app/polls-archive'}>
            <InboxIcon />
            Архив
          </StyledArchiveLink>
          <PollsGridWrapper>
            <PollsGrid>
              {$pollsData
                ?.filter((item) => !item.is_closed)
                .map((item) => (
                  <Link key={item.poll_id} to={`/app/tests/${item.poll_id}/main`}>
                    <AppPoleCard pollData={item} fetchData={fetchData} />
                  </Link>
                ))}
            </PollsGrid>
            <CustomPagination
              pageSize={pageSize}
              totalPages={totalPages}
              currentPage={currPage}
              handlePageChange={handlePageChange}
              handlePageSizeChange={handlePageSizeChange}
            />
          </PollsGridWrapper>
        </ContentWrapper>
      </StyledAppContentWrapper>
    );
  };

  return (
    <>
      <AppPollFilters handleCreateModalOpen={setIsCreateModalOpen} setPollData={setPollsData} />
      {loading ? (
        <StyledAppContentWrapper>
          <CircularProgress />
        </StyledAppContentWrapper>
      ) : (
        renderAppContent()
      )}
      <FrmCreatePoll
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title={surveySettings.survey.popUpTitle}
        buttons={surveySettings.survey.surveyButtons}
      />
    </>
  );
};

export default AppPage;
