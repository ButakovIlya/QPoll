import { createEvent, createStore } from 'effector';

const $polls = createStore([]);

const setPollsData = createEvent('Set polls data');

$polls.on(setPollsData, (_, newArray) => newArray);

// $polls.watch((state) => console.log(`Polls Effector store:`, state));

export { $polls, setPollsData };
