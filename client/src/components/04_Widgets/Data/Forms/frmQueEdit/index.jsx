import { DeleteOutline } from '@mui/icons-material';
import {
  Box,
  Checkbox,
  Divider,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import {
  addOptionRequest,
  changeOptionOrderRequest,
  changeOptionRequest,
  deleteOptionRequest,
  getAllOptionsRequest,
  handleChangeAnswerRequest,
  handleChangeQuestionInfoRequest,
} from './api/apiRequests';
import { deleteImageFx } from './model/delete-image';
import { QueBtnWrapper, QueSettingsWrapper, StyledDragIndicator } from './styled';

import PoleImageUpload from '@/components/06_Entities/PollImageUpload';
import QueTypeSelect from '@/components/06_Entities/QueTypeSelect';
import CustomSwitch from '@/components/07_Shared/UIComponents/Buttons/switch';
import InvisibleLabeledField from '@/components/07_Shared/UIComponents/Fields/invisibleLabeledField';
import DraggableList from '@/components/07_Shared/UIComponents/Layouts/draggableList';
import usePollData from '@/hooks/usePollData';

const FrmQueEdit = ({ question, setSelectedQuestion, onQuestionUpdate }) => {
  const { id } = useParams();
  const { t } = useTranslation();
  const [editedQuestion, setEditedQuestion] = useState(question);
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState([]);
  const [questionType, setQuestionType] = useState('Один ответ');
  const [isFreeResponse, setIsFreeResponse] = useState(false);
  const [isRequired, setIsRequired] = useState(false);
  const [fieldChangeTimeout, setFieldChangeTimeout] = useState(null);
  const { pollType, pollStatus } = usePollData(id);

  useEffect(() => {
    const correctOptions = question?.answer_options?.filter((option) => option.is_correct);
    setSelectedOption(correctOptions?.length ? correctOptions?.map((option) => option.id) : []);
    setEditedQuestion(question);
  }, [question]);

  useEffect(() => {
    const hasFreeResponse = options.some((option) => option.is_free_response);
    setIsFreeResponse(hasFreeResponse);
  }, [options]);

  const handleOptionSelect = async (e, q_id) => {
    const value = e.target.value;
    if (question.has_multiple_choices) {
      if (selectedOption.includes(Number(value))) {
        setSelectedOption(selectedOption?.filter((item) => item !== Number(value)));
        await handleChangeAnswerRequest(id, q_id, value, 0);
      } else {
        setSelectedOption([...selectedOption, Number(value)]);
        await handleChangeAnswerRequest(id, q_id, value, 1);
      }
    } else {
      setSelectedOption([value]);
      await handleChangeAnswerRequest(id, q_id, value, 1);
    }
    fetchOptions();
  };

  const fetchOptions = async () => {
    if (question.is_free && pollType !== 'Викторина') {
      setOptions([]);
    } else {
      await getAllOptionsRequest(id, question.id).then((res) => {
        setOptions(res.data);
        const hasFreeResponse = res.data.some((option) => option.is_free_response);
        setIsFreeResponse(hasFreeResponse);

        const correctOptions = res.data
          .filter((option) => option.is_correct)
          .map((item) => item.id);
        setSelectedOption(correctOptions);
      });
    }
  };

  useEffect(() => {
    fetchOptions();
    setIsRequired(question.is_required);
  }, [id, question]);

  const handleFieldChange = async (fieldName, value, q_id) => {
    if (fieldChangeTimeout) {
      clearTimeout(fieldChangeTimeout);
    }

    const updatedQuestion = { ...editedQuestion, [fieldName]: value };
    setEditedQuestion(updatedQuestion);
    const newTimeout = setTimeout(async () => {
      await handleChangeQuestionInfoRequest(fieldName, value, id, q_id);
      if (onQuestionUpdate) onQuestionUpdate(q_id, fieldName, value);
    }, 1000);

    setFieldChangeTimeout(newTimeout);
  };

  const handleOptionChange = async (fieldName, value, opt_id, q_id) => {
    if (fieldChangeTimeout) {
      clearTimeout(fieldChangeTimeout);
    }
    const newTimeout = setTimeout(async () => {
      await changeOptionRequest(id, q_id, opt_id, fieldName, value);
    }, 1000);
    setFieldChangeTimeout(newTimeout);
    setOptions((prevOptions) =>
      prevOptions.map((option) =>
        option.id === opt_id ? { ...option, [fieldName]: value } : option,
      ),
    );
  };

  const handleDeleteOption = async (opt_id, q_id) => {
    if (pollStatus) return;
    await deleteOptionRequest(id, q_id, opt_id);
    fetchOptions();
  };

  const handleAddOption = async (param) => {
    await addOptionRequest(id, question.id, param).then(() => fetchOptions());
  };

  const onDragEnd = async (result) => {
    const { source, destination } = result;
    const newItems = Array.from(options);

    if (
      !destination ||
      (source.droppableId === destination.droppableId && source.index === destination.index)
    ) {
      return;
    }
    const isLastFreeResponse = newItems[newItems.length - 1].is_free_response;

    if (destination.index === newItems.length - 1 && isLastFreeResponse) {
      return;
    }

    const [reorderedItem] = newItems.splice(source.index, 1);
    newItems.splice(destination.index, 0, reorderedItem);
    setOptions(newItems);
    await changeOptionOrderRequest(id, question.id, newItems);
  };

  const handleImageDelete = (q_id) => {
    deleteImageFx({ id, q_id });
  };

  return (
    <Box sx={{ padding: '0 15px' }}>
      <PoleImageUpload
        image={question?.image}
        onFileSelect={(e) => handleFieldChange('image', e, question.id)}
        handleDelete={() => handleImageDelete(question.id)}
        disabled={pollStatus}
      />
      <QueSettingsWrapper>
        <InvisibleLabeledField
          placeholder="Введите заголовок"
          value={editedQuestion.name || ''}
          handleChange={(e) => {
            handleFieldChange('name', e, question.id);
            if (onQuestionUpdate) onQuestionUpdate(question.id, 'name', e);
          }}
          disabled={pollStatus}
        />
        <InvisibleLabeledField
          placeholder="Введите описание"
          value={editedQuestion.info || ''}
          handleChange={(e) => {
            handleFieldChange('info', e, question.id);
            if (onQuestionUpdate) onQuestionUpdate(question.id, 'info', e);
          }}
          disabled={pollStatus}
        />
        <QueTypeSelect
          question={editedQuestion}
          questionType={questionType}
          setQuestionType={setQuestionType}
          setQuestion={setSelectedQuestion}
        />
      </QueSettingsWrapper>
      <Divider style={{ margin: '30px 0' }} />
      <DraggableList
        disabled={pollStatus}
        items={options}
        onDragEnd={onDragEnd}
        pollType={pollType}
        renderItem={(item) => (
          <>
            <StyledDragIndicator isFree={item.is_free_response} status={pollStatus} />
            {pollType === 'Викторина' &&
              (question.has_multiple_choices ? (
                <Box sx={{ width: '24px', height: '24px', marginRight: '15px' }}>
                  <FormControlLabel
                    key={item.id}
                    control={
                      <Checkbox
                        checked={selectedOption.includes(item.id)}
                        onChange={(e) => handleOptionSelect(e, question.id)}
                        value={item.id}
                        sx={{ width: '24px', height: '24px' }}
                        disabled={pollStatus}
                      />
                    }
                  />
                </Box>
              ) : (
                <RadioGroup
                  value={selectedOption[0] || ''}
                  onChange={(e) => handleOptionSelect(e, question.id)}
                  sx={{ width: '24px', height: '24px', marginRight: '15px' }}
                >
                  <FormControlLabel
                    control={<Radio sx={{ width: '24px', height: '24px' }} />}
                    value={item.id.toString()}
                    disabled={pollStatus}
                  />
                </RadioGroup>
              ))}

            {item.is_free_response ? (
              pollType === 'Опрос' ? (
                <p>Другое</p>
              ) : (
                <InvisibleLabeledField
                  placeholder="Введите правильный ответ"
                  value={item.name || ''}
                  handleChange={(e) => handleOptionChange('name', e, item.id, question.id)}
                  disabled={pollStatus}
                />
              )
            ) : (
              <InvisibleLabeledField
                placeholder="Начните вводить"
                value={item.name || ''}
                handleChange={(e) => handleOptionChange('name', e, item.id, question.id)}
                disabled={pollStatus}
              />
            )}
            <Box sx={{ display: 'flex', alignItems: 'center', columnGap: '5px' }}>
              <DeleteOutline
                sx={{ cursor: 'pointer' }}
                onClick={() => handleDeleteOption(item.id, question.id)}
              />
            </Box>
          </>
        )}
      />
      <QueBtnWrapper>
        <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10px' }}>
          {options.length === 0 && !question.is_free && (
            <Typography>Вы не создали ни одного варианта ответа</Typography>
          )}
          {!question.is_free && (
            <Box sx={{ display: 'flex', alignItems: 'center', columnGap: '10px' }}>
              <button
                style={{ maxWidth: '100%' }}
                onClick={() => handleAddOption()}
                disabled={pollStatus}
              >
                {t('button.addAnswer')}
              </button>
              {!isFreeResponse && (
                <>
                  <span>или</span>
                  <button
                    style={{ maxWidth: '100%' }}
                    onClick={() => handleAddOption('is_free')}
                    disabled={pollStatus}
                  >
                    {t('button.addFreeAnswer')}
                  </button>
                </>
              )}
            </Box>
          )}
        </Box>
        <Box>
          <FormControlLabel
            label="Обязательный вопрос"
            control={
              <CustomSwitch
                disabled={pollStatus}
                onChange={() => {
                  setIsRequired((prev) => !prev);
                  handleFieldChange('is_required', !isRequired, question.id);
                }}
                checked={isRequired}
              />
            }
            sx={{ flexDirection: 'row-reverse', margin: 0 }}
          />
        </Box>
      </QueBtnWrapper>
    </Box>
  );
};

export default React.memo(FrmQueEdit);
