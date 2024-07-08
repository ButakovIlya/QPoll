import PollResultsSVG from '@assets/Analytics.svg';
import BarChartIcon from '@mui/icons-material/BarChart';
import PieChartIcon from '@mui/icons-material/PieChart';
import { MenuItem } from '@mui/material';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { v4 } from 'uuid';

import { getPollAnswersFx, getPollResultsFx } from './model/get-results';
import { ResultsGridWrapper, SettingsWrapper, StldSelect, Wrapper } from './styled';

import PollResultCard from '@/components/05_Features/Data/Cards/pollResCard';
import GenExcelResults from '@/components/06_Entities/genExcelResults';
import NoDataHelper from '@/components/07_Shared/UIComponents/Utils/Helpers/noDataHelper';
import config from '@/config';
import usePageTitle from '@/hooks/usePageTitle';

const PollResultsPage = () => {
  usePageTitle('pollres');
  const { id } = useParams();
  const [questions, setQuestions] = useState([]);
  const [chartType, setChartType] = useState('pie');
  const [isResults, setIsResults] = useState(false);
  const [answers, setAnswers] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      const data = await getPollResultsFx({ id });
      const answers = await getPollAnswersFx({ id });
      setAnswers(answers);
      setQuestions(data.questions);
      setIsResults(data.participants_quantity > 0);
    };
    fetchResults();
    const parsed_id = id.replace(/-/g, '');
    const socket = new WebSocket(`ws://${config.serverUrl.wsMain}:9000/ws/${parsed_id}/`);

    socket.onmessage = function (event) {
      const { message } = JSON.parse(event.data);
      console.log(message);
      if (message.content === 'my_poll_stats') {
        setQuestions(message.data.questions);
        setIsResults(message.data.participants_quantity > 0);
      } else if (message.content === 'my_poll_users_votes') {
        setAnswers(message.data);
      }
    };

    return () => {
      socket.close();
    };
  }, [id]);

  const handleChartTypeChange = (event) => setChartType(event.target.value);

  return isResults ? (
    <Wrapper>
      <SettingsWrapper>
        <StldSelect value={chartType} onChange={handleChartTypeChange} displayEmpty>
          <MenuItem value="pie">
            <PieChartIcon /> Pie Chart
          </MenuItem>
          <MenuItem value="bar">
            <BarChartIcon /> Bar Chart
          </MenuItem>
        </StldSelect>
        <GenExcelResults questions={questions} data={answers} />
      </SettingsWrapper>
      <ResultsGridWrapper>
        {questions.map((item) => (
          <PollResultCard key={v4()} data={item} chartType={chartType} answers={answers} />
        ))}
      </ResultsGridWrapper>
    </Wrapper>
  ) : (
    <NoDataHelper
      title="Результатов еще нет"
      description="Результаты появятся после первого прохождения опроса"
      image={PollResultsSVG}
    />
  );
};

export default PollResultsPage;
