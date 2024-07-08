import { useUnit } from 'effector-react';
import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { fetchPollQuestions } from '../ConductionPoll/model/fetch-questions';
import { getRemainingTimeFx } from '../ConductionPoll/model/get-remaining-time';
import { sendAnswersRequestFx } from '../ConductionPoll/model/send-answers';
import { startConductionFx } from '../ConductionPoll/model/start-conduction';
import { $answersStore, resetAnswers } from '../ConductionPoll/store/answer-store';
import {
  ConductionBackgroundWrapper,
  ConductionWrapper,
  VoteEndedText,
} from '../ConductionPoll/styled';

import ConductionHeader from '@/components/04_Widgets/Content/Display/conductionHeader';
import QueBlock from '@/components/04_Widgets/Content/Interactive/queBlock';
import FrmQuickPollRegister from '@/components/04_Widgets/Data/Forms/frmQuickPollRegister';
import Header from '@/components/04_Widgets/Navigation/Menus/mainHeader';
import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import Timer from '@/components/07_Shared/UIComponents/Utils/Helpers/timer';
import { useAlert } from '@/hooks/useAlert';
import useAuth from '@/hooks/useAuth';
import usePageTitle from '@/hooks/usePageTitle';
import { shuffleArray } from '@/utils/js/shuffleArray';

const FastConductionPollPage = () => {
  usePageTitle('conduction');
  const { id } = useParams();
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();
  const { showAlert } = useAlert();
  const answers = useUnit($answersStore);
  const [pollData, setPollData] = useState({});
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [newPollStarted, setNewPollStarted] = useState(false);
  const [remainingTime, setRemainingTime] = useState('');
  const [isTextLong, setIsTextLong] = useState(false);
  const [isSubmitEnabled, setIsSubmitEnabled] = useState(true);

  const getRemainingTime = async () => {
    const formId = localStorage.getItem('voting_form_id');
    const data = await getRemainingTimeFx({ id, formId });
    if (data) {
      setRemainingTime(data.voting_time_left_str);
      if (Number(data.id) === Number(formId)) {
        setNewPollStarted(true);
        setIsCollapsed(false);
      }
    } else {
      setNewPollStarted(false);
      setIsCollapsed(true);
    }
  };

  useEffect(() => {
    const pollDataRequest = async () => {
      const data = await fetchPollQuestions(id);
      if (data !== undefined) {
        const formId = localStorage.getItem('voting_form_id');
        if (data.poll_setts.completion_time !== null && formId) getRemainingTime();
        if (data.mix_questions) data.questions = shuffleArray(data.questions);

        setIsCollapsed(true);
        setPollData(data);
      } else {
        navigate('/not-found');
      }
    };
    pollDataRequest();
  }, [id]);

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

  const handleContextMenu = (e) => e.preventDefault();

  const handleSubmit = async (isTimeEnd = false) => {
    const formId = localStorage.getItem('voting_form_id');
    await sendAnswersRequestFx({ answers, id, isTimeEnd, formId });
    resetAnswers();
    localStorage.removeItem('answersStore');
    localStorage.removeItem('voting_form_id');
    if (isTimeEnd) {
      showAlert(
        'Время прохождения опроса вышло. Отмеченные варианты ответов были записаны !',
        'info',
      );
    } else {
      showAlert('Ваш голос успешно записан!', 'success');
    }
    setTimeout(() => {
      // navigate('/polls');
      navigate('/');
    }, 1500);

    setFormSubmitted(true);
  };

  const handleTimeEnd = async () => await handleSubmit(true);

  const handleStart = async (data) => {
    resetAnswers();
    await startConductionFx({ id, data }).then((res) => {
      localStorage.setItem('voting_form_id', res.data.id);
      setRemainingTime(res.data.voting_time_left_str);
      setIsCollapsed(false);
      setNewPollStarted(true);
    });
  };

  useEffect(() => {
    if (formSubmitted || newPollStarted) {
      resetAnswers();
      setFormSubmitted(false);
    }
  }, [formSubmitted, newPollStarted]);

  return (
    <ConductionBackgroundWrapper onContextMenu={handleContextMenu}>
      <Header isMainPage={false} />
      <ConductionWrapper>
        <ConductionHeader data={pollData} />
        {!newPollStarted && pollData?.opened_for_voting ? (
          <FrmQuickPollRegister
            isCollapsed={isCollapsed}
            handleStart={handleStart}
            pollData={pollData}
          />
        ) : (
          !pollData?.opened_for_voting && <VoteEndedText>Опрос завершен !</VoteEndedText>
        )}
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
      </ConductionWrapper>
    </ConductionBackgroundWrapper>
  );
};

export default FastConductionPollPage;
