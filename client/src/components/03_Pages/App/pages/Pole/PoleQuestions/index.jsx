import { Box, useMediaQuery } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import {
  handleCreateQuestionRequest,
  handleGetAllQuestionRequest,
  handleGetQuestionInfoRequest,
} from './api/apiRequests';
import { ListWrapper, LoaderWrapper } from './styled';

import FrmQueEdit from '@/components/04_Widgets/Data/Forms/frmQueEdit';
import PollQuestionsList from '@/components/05_Features/DataDisplay/Out/PollQuestionsList';
import PoleCreateFirstQuestion from '@/components/05_Features/UIComponents/Utils/PollCreateFirstQuestion';
import CLoader from '@/components/07_Shared/UIComponents/Utils/Helpers/loader';
import usePageTitle from '@/hooks/usePageTitle';

const _settings = {
  title: 'Вы не создали ни одного вопроса',
  buttonCaption: 'Создать вопрос',
};

const PoleQuestionsPage = () => {
  usePageTitle('qsettings');
  const { id } = useParams();
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedQuestion, setSelectedQuestion] = useState({});
  const matches = useMediaQuery('(max-width:1000px)');

  useEffect(() => {
    handleGetAllQuestionRequest(id)
      .then((res) => setQuestions(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  const handleCreateQuestion = useCallback(async () => {
    await handleCreateQuestionRequest(id).then(() =>
      handleGetAllQuestionRequest(id).then((res) => setQuestions(res.data)),
    );
  }, [id]);

  const handleSelectQuestion = useCallback(
    async (question_id) => {
      await handleGetQuestionInfoRequest(id, question_id).then((res) =>
        setSelectedQuestion(res.data),
      );
    },
    [id],
  );

  const handleQuestionUpdate = (questionId, fieldName, value) => {
    setQuestions((prevQuestions) =>
      prevQuestions.map((q) => (q.id === questionId ? { ...q, [fieldName]: value } : q)),
    );
  };

  const renderQuestionList = () => {
    return questions.length === 0 ? (
      <PoleCreateFirstQuestion settings={_settings} handleCreateQuestion={handleCreateQuestion} />
    ) : (
      <ListWrapper>
        <Box sx={{ width: matches ? '100%' : '25%' }}>
          <PollQuestionsList
            questions={questions}
            onSelectQuestion={handleSelectQuestion}
            onAddQuestion={handleCreateQuestion}
            selectedQuestion={selectedQuestion}
            setQuestions={setQuestions}
            setSelected={setSelectedQuestion}
            onQuestionUpdate={handleQuestionUpdate}
          />
        </Box>
        <Box sx={{ width: '75%', display: matches ? 'none' : 'block' }}>
          {Object.keys(selectedQuestion).length > 0 && (
            <FrmQueEdit
              question={selectedQuestion}
              setSelectedQuestion={setSelectedQuestion}
              onQuestionUpdate={handleQuestionUpdate}
            />
          )}
        </Box>
      </ListWrapper>
    );
  };

  return (
    <LoaderWrapper matches={matches}>{loading ? <CLoader /> : renderQuestionList()}</LoaderWrapper>
  );
};

export default PoleQuestionsPage;
