import { useUnit } from 'effector-react';
import { useCallback, useEffect } from 'react';

import {
  fetchPollDataFx,
  isMultipleStore,
  pollDataStore,
  pollStatusStore,
  pollTypeStore,
} from '@/api/store/poll-data';

const usePollData = (pollId) => {
  const pollData = useUnit(pollDataStore);
  const pollStatus = useUnit(pollStatusStore);
  const pollType = useUnit(pollTypeStore);
  const isMultiple = useUnit(isMultipleStore);

  const fetchDataCallback = useCallback(() => {
    fetchPollDataFx(pollId);
  }, [pollId]);

  useEffect(() => {
    fetchDataCallback();
  }, [fetchDataCallback]);

  return { pollType, pollStatus, isMultiple, pollData };
};

export default usePollData;
