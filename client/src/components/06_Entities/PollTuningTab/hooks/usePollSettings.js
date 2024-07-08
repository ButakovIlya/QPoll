import { useCallback, useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { pathcPollSettingsFx } from '../model/patch-poll';

const usePollSettings = (initialSettings) => {
  const { id } = useParams();
  const [settings, setSettings] = useState(initialSettings);

  useEffect(() => {
    setSettings(initialSettings);
  }, [initialSettings]);

  const handleSwitchChange = useCallback(
    (field) => async (event) => {
      const value = event.target.checked;
      pathcPollSettingsFx({ id, value, field });
      setSettings((prev) => ({ ...prev, [field]: value }));
    },
    []
  );

  return [settings, handleSwitchChange];
};

export default usePollSettings;
