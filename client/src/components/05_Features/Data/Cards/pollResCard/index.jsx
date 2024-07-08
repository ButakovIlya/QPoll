import { Box } from '@mui/material';
import { BarChart, PieChart } from '@mui/x-charts';
import { useState } from 'react';

import FrmOtherResults from '../../Forms/frmOtherResults';

import { CardAnswersCount, CardHeading, CardInfoWrapper, CardWrapper, InfoButton } from './styled';

const PollResultCard = ({ data, chartType, answers }) => {
  const [infoOpen, setInfoOpen] = useState(false);

  const renderChart = () => {
    const chartData = data.answer_options.map((option) => ({
      id: option.id,
      value: option.votes_quantity,
      label: option.is_free_response ? 'Другое' : option.name,
    }));

    const xAxisData = data.answer_options.map((opt) => opt?.name);

    const barChartData = data.answer_options.map((option) => option.votes_quantity);

    switch (chartType) {
      case 'bar':
        return (
          <BarChart
            series={[{ data: barChartData }]}
            xAxis={[{ data: xAxisData, scaleType: 'band' }]}
            width={450}
            height={200}
          />
        );
      case 'pie':
      default:
        return (
          <PieChart
            series={[{ data: chartData }]}
            width={450}
            height={200}
            slotProps={{
              legend: {
                labelStyle: {
                  text: {
                    maxWidth: '70px',
                  },
                  maxWidth: '70px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  display: '-webkit-box',
                  WebkitBoxOrient: 'vertical',
                  WebkitLineClamp: 2,
                },
              },
            }}
          />
        );
    }
  };

  return (
    <CardWrapper>
      <CardInfoWrapper>
        <Box>
          <CardHeading>{data.name ?? ''}:</CardHeading>
          <CardAnswersCount>Ответов: {data.votes_quantity}</CardAnswersCount>
        </Box>
        <InfoButton onClick={() => setInfoOpen(true)}>Подробнее</InfoButton>
      </CardInfoWrapper>
      {renderChart()}
      <FrmOtherResults
        open={infoOpen}
        onClose={() => setInfoOpen(false)}
        data={data}
        answers={answers}
      />
    </CardWrapper>
  );
};

export default PollResultCard;
