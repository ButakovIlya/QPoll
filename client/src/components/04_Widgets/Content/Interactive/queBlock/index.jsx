import {
  Checkbox,
  FormControlLabel,
  Radio,
  RadioGroup,
  TextField,
  Typography,
} from '@mui/material';
import { useUnit } from 'effector-react';
import { useEffect, useState } from 'react';

import { StyledFormControl } from './styled';

import {
  $answersStore,
  updateAnswer,
  updateMultipleAnswer,
} from '@/components/03_Pages/Polls/ConductionPoll/store/answer-store';
import { shuffleArray } from '@/utils/js/shuffleArray';

const QueBlock = ({ question, isMixed, setIsLong }) => {
  const answers = useUnit($answersStore);
  const [selectedValue, setSelectedValue] = useState('');
  const [selectedValues, setSelectedValues] = useState([]);
  const [fieldValue, setFieldValue] = useState('');
  const [options, setOptions] = useState(question.answer_options ?? []);
  const [isTextLong, setIsTextLong] = useState(false);

  useEffect(() => {
    if (question.has_multiple_choices) {
      const selectedOpts = answers
        .filter((ans) => ans.question === question.id)
        .map((ans) => ans.answer_option);
      setSelectedValues(selectedOpts);
    } else {
      const selectedOpt = answers.find((ans) => ans.question === question.id);
      if (selectedOpt) {
        setSelectedValue(selectedOpt.answer_option.toString());
      }
    }

    const textAnswer = answers.find((ans) => ans.question === question.id && ans.text);
    if (textAnswer) {
      setFieldValue(textAnswer.text);
    }
  }, [answers, question.id, question.has_multiple_choices]);

  useEffect(() => {
    if (isMixed) {
      const shuffled = shuffleArray([...question.answer_options]);
      const index = shuffled.findIndex((option) => option.order_id === 16);
      if (index !== -1) {
        const [item] = shuffled.splice(index, 1);
        shuffled.push(item);
      }
      setOptions(shuffled);
    }
  }, [isMixed, question]);

  const handleMultipleChoiceChange = (event, opt_id) => {
    const { checked } = event.target;
    setFieldValue('');
    if (checked) {
      setSelectedValues((prev) => [...prev, opt_id]);
    } else {
      setSelectedValues((prev) => prev.filter((id) => id !== opt_id));
    }
    updateMultipleAnswer({ answer_option: opt_id, question: question.id, selected: checked });
    setIsTextLong(false);
    setIsLong(false);
  };

  const handleRadioChange = (event) => {
    const { value } = event.target;
    setFieldValue('');
    setSelectedValue(value);
    updateAnswer({ answer_option: Number(value), question: question.id });
    setIsTextLong(false);
    setIsLong(false);
  };

  const handleTextChange = (event, opt_id) => {
    const { value } = event.target;
    setSelectedValues([]);
    setFieldValue(value);
    updateMultipleAnswer({ answer_option: opt_id, question: question.id, text: value });
    setIsTextLong(value.length > 100);
    setIsLong(value.length > 100);
  };

  return (
    <StyledFormControl component="fieldset">
      <Typography sx={{ fontSize: '15px' }}>{question.name}</Typography>
      <Typography sx={{ fontSize: '13px', color: '#868686' }}>{question.info}</Typography>
      {question.is_free ? (
        options.map((option) => (
          <TextField
            key={option.id}
            label="Мой ответ"
            variant="outlined"
            fullWidth
            error={isTextLong}
            value={fieldValue || ''}
            id={String(option.id)}
            helperText={isTextLong ? 'Длина ответа не должна превышать 100 символов !' : ''}
            onChange={(e) => handleTextChange(e, option.id)}
            sx={{ marginTop: '10px' }}
          />
        ))
      ) : (
        <RadioGroup
          aria-label={question.name}
          name="radio-buttons-group"
          value={selectedValue}
          onChange={handleRadioChange}
        >
          {options.map((option) =>
            option.is_free_response ? (
              <TextField
                key={option.id}
                label="Введите ваш ответ"
                variant="outlined"
                fullWidth
                error={isTextLong}
                value={fieldValue || ''}
                helperText={isTextLong ? 'Длина ответа не должна превышать 100 символов !' : ''}
                onChange={(e) => handleTextChange(e, option.id)}
                sx={{ marginTop: '10px' }}
              />
            ) : (
              <FormControlLabel
                key={option.id}
                value={option.id}
                control={
                  question.has_multiple_choices ? (
                    <Checkbox
                      checked={selectedValues?.includes(option.id)}
                      onChange={(e) => handleMultipleChoiceChange(e, option.id)}
                    />
                  ) : (
                    <Radio checked={selectedValue === option.id.toString()} />
                  )
                }
                label={option.name}
              />
            ),
          )}
        </RadioGroup>
      )}
    </StyledFormControl>
  );
};

export default QueBlock;
