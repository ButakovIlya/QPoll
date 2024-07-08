import { useCallback, useState } from 'react';

const useTabs = (defaultValue = 0) => {
  const [value, setValue] = useState(defaultValue);

  const handleChange = useCallback((event, newValue) => {
    setValue(newValue);
  }, []);

  return [value, handleChange];
};

export default useTabs;
