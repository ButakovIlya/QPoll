import { createEvent, createStore } from 'effector';

export const updateAnswer = createEvent();
export const updateMultipleAnswer = createEvent();
export const resetAnswers = createEvent();
const initialState = JSON.parse(localStorage.getItem('answersStore')) || [];

const saveStateToLocalStorage = (state) => {
  localStorage.setItem('answersStore', JSON.stringify(state));
};

export const $answersStore = createStore(initialState)
  .on(updateMultipleAnswer, (state, { question, answer_option, text = null, selected }) => {
    if (text !== null) {
      if (text === '') {
        return state.filter((answer) => !(answer.question === question && answer.text !== null));
      }
      const newState = state.filter((answer) => answer.question !== question);
      return [...newState, { answer_option, question, text }];
    } else {
      const filteredState = state.filter(
        (answer) => !(answer.question === question && answer.text),
      );

      const existingAnswerIndex = filteredState.findIndex(
        (answer) => answer.question === question && answer.answer_option === answer_option,
      );
      if (selected) {
        if (existingAnswerIndex === -1) {
          return [...filteredState, { answer_option, question }];
        }
      } else if (existingAnswerIndex !== -1) {
        return filteredState.filter(
          (answer) => !(answer.question === question && answer.answer_option === answer_option),
        );
      }
      return filteredState;
    }
  })
  .on(updateAnswer, (state, payload) => {
    const answerIndex = state.findIndex((answer) => answer.question === payload.question);
    if (answerIndex > -1) {
      return state.map((answer) => (answer.question === payload.question ? payload : answer));
    } else {
      return [...state, payload];
    }
  })
  .reset(resetAnswers);

$answersStore.watch(saveStateToLocalStorage);

// $answersStore.watch((state) => console.log(state));
