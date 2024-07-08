import { v4 } from 'uuid';

import PollResHead from '@/components/05_Features/Content/Display/PollResHead';
import ConductionResCrd from '@/components/05_Features/Data/Cards/conductionResCrd';
import usePageTitle from '@/hooks/usePageTitle';

const PollResult = ({ data }) => {
  usePageTitle('results');
  const { questions, result, results } = data;

  return (
    <>
      <PollResHead res={results} data={data} />
      {questions.map((item) => (
        <ConductionResCrd key={v4()} question={item} answers={result.answers} />
      ))}
    </>
  );
};

export default PollResult;
