import { CheckBox, RadioButtonChecked, ShortText } from '@mui/icons-material';
import { ListItemIcon, ListItemText, MenuItem } from '@mui/material';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { changePollTypeFx } from './models/change-poll-type';
import { TypeSelect } from './styled';

import usePollData from '@/hooks/usePollData';

const QueTypeSelect = ({ question, questionType, setQuestionType, setQuestion }) => {
  const { id } = useParams();
  const { pollStatus } = usePollData(id);

  const queTypes = [
    {
      caption: 'Один ответ',
      name: 'single',
      icon: <RadioButtonChecked fontSize="small" />,
      type: { has_multiple_choices: false, is_free: false },
    },
    {
      caption: 'Несколько ответов',
      name: 'multiple',
      icon: <CheckBox fontSize="small" />,
      type: { has_multiple_choices: true, is_free: false },
    },
    {
      caption: 'Развернутый ответ',
      name: 'free',
      icon: <ShortText fontSize="small" />,
      type: { is_free: true, has_multiple_choices: false },
    },
  ];

  useEffect(() => {
    let initialQuestionType = 'single';
    if (question.is_free) {
      initialQuestionType = 'free';
    } else if (question.has_multiple_choices) {
      initialQuestionType = 'multiple';
    }

    const initialQuestionTypeObject = queTypes.find((item) => item.name === initialQuestionType);

    // Устанавливаем отображаемую подпись для типа вопроса
    setQuestionType(initialQuestionTypeObject.caption);
  }, [question]);

  const handleTypeChange = async (e) => {
    const selectedType = e.target.value;
    setQuestionType(selectedType);

    const selectedTypeObject = queTypes.find((item) => item.caption === selectedType);
    if (selectedTypeObject) {
      await changePollTypeFx(id, question.id, selectedTypeObject.type).then((res) =>
        setQuestion(res.data),
      );
    }
  };

  return (
    <TypeSelect value={questionType} onChange={(e) => handleTypeChange(e)} disabled={pollStatus}>
      {queTypes.map((item) => (
        <MenuItem key={item.name} value={item.caption}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.caption} />
        </MenuItem>
      ))}
    </TypeSelect>
  );
};

export default QueTypeSelect;
