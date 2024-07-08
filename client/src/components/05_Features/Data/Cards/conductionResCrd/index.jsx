import { Typography } from '@mui/material';

import { OptionName, OptionsWrapper, StyledFormControl, StyledOption } from './styled';

const ConductionResCrd = ({ question = {}, answers }) => {
  const options = question.answer_options ?? [];

  return (
    <StyledFormControl component="fieldset">
      <Typography>{question.name}</Typography>
      <OptionsWrapper>
        {options.map((item) => {
          const foundAnswer = answers.find((ans) => ans.answer_option === item.id);
          const isCorrect = foundAnswer ? foundAnswer.points === 1 : null;
          return (
            <StyledOption key={item.id} isCorrect={isCorrect}>
              <OptionName>
                {question.is_free || item.order_id === 16 ? item.text : item.name}
              </OptionName>
            </StyledOption>
          );
        })}
      </OptionsWrapper>
    </StyledFormControl>
  );
};

export default ConductionResCrd;
