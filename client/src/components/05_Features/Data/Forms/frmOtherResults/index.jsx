import { Dialog, DialogContent, DialogTitle, Typography } from '@mui/material';
import { v4 } from 'uuid';

import { NameWrapper } from './styled';

import { nameReducer } from '@/utils/js/nameReducer';

const FrmOtherResults = ({ open, onClose, data, answers }) => {
  const filteredData = data.answer_options.filter((option) => option.is_free_response);

  const filteredAnswers = answers.answers
    .map((userAnswer) => {
      const answer = userAnswer.answers.find((item) => item.answers.question === data.id);
      return answer
        ? {
            profile: userAnswer.profile,
            text:
              answer.answers.answer_option !== null
                ? answer.answers.answer_option
                : answer.answers.text,
          }
        : null;
    })
    .filter(Boolean);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      scroll="paper"
      maxWidth="sm"
      fullWidth
      sx={{ maxHeight: '500px' }}
    >
      <DialogTitle>Результаты</DialogTitle>
      <DialogContent dividers>
        {filteredAnswers.length > 0 ? (
          filteredAnswers.map((item, index) => (
            <NameWrapper key={v4()} isLower={index < data.length - 1}>
              <Typography variant="body1" component="p">
                {nameReducer(
                  `${item.profile.surname} ${item.profile.name} ${item.profile.patronymic}`,
                )}
              </Typography>
              <Typography variant="body2" component="p">
                {item.text}
              </Typography>
            </NameWrapper>
          ))
        ) : (
          <p>Ответов &apos;Другое&apos; не найдено</p>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default FrmOtherResults;
