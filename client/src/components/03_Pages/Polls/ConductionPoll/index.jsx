import { useUnit } from 'effector-react';
import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import PollResult from '../PollResult';

import { fetchPollQuestions } from './model/fetch-questions';
import { getRemainingTimeFx } from './model/get-remaining-time';
import { sendAnswersRequestFx } from './model/send-answers';
import { startConductionFx } from './model/start-conduction';
import { $answersStore, resetAnswers } from './store/answer-store';
import {
  ConductionBackgroundWrapper,
  ConductionWrapper,
  StartBtnWrapper,
  VoteEndedText,
} from './styled';

import ConductionHeader from '@/components/04_Widgets/Content/Display/conductionHeader';
import QueBlock from '@/components/04_Widgets/Content/Interactive/queBlock';
import Header from '@/components/04_Widgets/Navigation/Menus/mainHeader';
import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import Timer from '@/components/07_Shared/UIComponents/Utils/Helpers/timer';
import { useAlert } from '@/hooks/useAlert';
import useAuth from '@/hooks/useAuth';
import usePageTitle from '@/hooks/usePageTitle';
import { shuffleArray } from '@/utils/js/shuffleArray';

const ConductionPollPage = () => {
  usePageTitle('conduction');
  const { id } = useParams();
  const { isAuthenticated, isLoading } = useAuth();
  const { showAlert } = useAlert();
  const navigate = useNavigate();
  const answers = useUnit($answersStore);
  const [pollData, setPollData] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState({});
  const [isTextLong, setIsTextLong] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [isSubmitEnabled, setIsSubmitEnabled] = useState(true);
  const [remainingTime, setRemainingTime] = useState('');
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [newPollStarted, setNewPollStarted] = useState(false);

  const getRemainingTime = async () => {
    const data = await getRemainingTimeFx({ id });
    setRemainingTime(data.voting_time_left_str);
  };

  useEffect(() => {
    if (isLoading) return;
    const pollDataRequest = async () => {
      const data = await fetchPollQuestions(id);
      if (data) {
        if (data.poll_setts.completion_time !== null) getRemainingTime();

        if (
          (!data.is_revote_allowed && data.has_user_participated_in) ||
          isAuthenticated === false
        ) {
          navigate('/polls');
          return;
        }
        if (data.mix_questions) data.questions = shuffleArray(data.questions);
        setIsCollapsed(data.poll_setts?.completion_time !== null);
        if (data.has_user_started_voting) handleStart();
        setPollData(data);
      } else {
        navigate('/not-found');
      }
    };
    pollDataRequest();
  }, [isLoading, isAuthenticated, id]);

  useEffect(() => {
    const requiredQuestions = pollData.questions
      ?.filter((q) => q.is_required)
      .map((item) => item.id);
    const answersSelected = answers.map((item) => item.question);

    const areAllRequiredAnswered = requiredQuestions?.every((item) =>
      answersSelected.includes(item),
    );
    setIsSubmitEnabled(areAllRequiredAnswered);
  }, [pollData.questions, answers]);

  const handleSubmit = async (isTimeEnd = false) => {
    // await sendAnonymousAnswersFx({ answers, id, isTimeEnd });
    const response = await sendAnswersRequestFx({ answers, id, isTimeEnd });
    setResults(response.data);
    resetAnswers();
    localStorage.removeItem('answersStore');
    if (response.data.poll_type !== 'Викторина') {
      if (isTimeEnd) {
        showAlert(
          'Время прохождения опроса вышло. Отмеченные варианты ответов были записаны !',
          'info',
        );
      } else {
        showAlert('Ваш голос успешно записан!', 'success');
      }
      setTimeout(() => {
        navigate('/polls');
      }, 1500);
    } else {
      if (isTimeEnd) {
        showAlert(
          'Время прохождения опроса вышло. Отмеченные варианты ответов были записаны !',
          'info',
        );
      }
      setShowResults(true);
      setFormSubmitted(true);
    }
  };

  const handleTimeEnd = async () => await handleSubmit(true);

  const handleContextMenu = (e) => e.preventDefault();

  const handleStart = async () => {
    await startConductionFx({ id }).then((res) => {
      setRemainingTime(res.data.voting_time_left_str);
      setIsCollapsed(false);
      setNewPollStarted(true);
    });
  };

  useEffect(() => {
    if (formSubmitted || newPollStarted) {
      resetAnswers();
      setFormSubmitted(false);
      setNewPollStarted(false);
    }
  }, [formSubmitted, newPollStarted]);

  return (
    <ConductionBackgroundWrapper onContextMenu={handleContextMenu}>
      <Header isMainPage={false} />
      <ConductionWrapper>
        {showResults ? (
          <PollResult data={results} />
        ) : (
          <>
            <ConductionHeader data={pollData} />
            <AnimatePresence>
              {!isCollapsed && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.4 }}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    rowGap: '18px',
                    width: '100%',
                    alignItems: 'center',
                  }}
                >
                  {pollData?.poll_setts?.completion_time !== null && (
                    <Timer initialTime={remainingTime} onTimeEnd={() => handleTimeEnd()} />
                  )}
                  {pollData?.questions?.map((item) => (
                    <QueBlock
                      key={item.id}
                      question={item}
                      isMixed={pollData?.mix_options}
                      setIsLong={setIsTextLong}
                    />
                  ))}
                  <PrimaryButton
                    caption="Отправить"
                    handleClick={() => handleSubmit()}
                    disabled={!isSubmitEnabled || isTextLong}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </>
        )}
      </ConductionWrapper>
      {isCollapsed &&
      pollData?.poll_setts?.completion_time !== null &&
      pollData.opened_for_voting ? (
        <StartBtnWrapper>
          <PrimaryButton caption="Начать" handleClick={handleStart} />
        </StartBtnWrapper>
      ) : (
        <VoteEndedText>Опрос завершен !</VoteEndedText>
      )}
    </ConductionBackgroundWrapper>
  );
};

export default ConductionPollPage;
