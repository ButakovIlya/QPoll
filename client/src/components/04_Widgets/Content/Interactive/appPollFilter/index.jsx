import TuneIcon from '@mui/icons-material/Tune';
import { Button } from '@mui/material';
import TextField from '@mui/material/TextField';
import { AnimatePresence, motion } from 'framer-motion';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { filterPollsRequest } from './api/apiRequests';
import {
  FiltersWrapper,
  MobFiltersContent,
  MobFiltersWrapper,
  MobileFiltersWrapper,
  StyledStack,
  StyledStackWrapper,
} from './styled';

import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import FilterSelect from '@/components/07_Shared/UIComponents/Fields/filterSelect';
import { appFilterOptions } from '@/data/filters';
import useUserData from '@/hooks/useUserData';

const AppPollFilters = ({ handleCreateModalOpen = () => {}, setPollData = () => {} }) => {
  const { t } = useTranslation();
  const userData = useUserData();
  const [filters, setFilters] = useState({
    search: '',
    poll_type: 'Все типы',
    is_closed: 'Все статусы',
    group: 'Для всех',
  });
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    const adjustedValue = value === 'Все типы' || value === 'Все статусы' ? '' : value;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
    applyFilters(name, adjustedValue);
  };

  const applyFilters = async (field, value) => {
    await filterPollsRequest(field, value, setPollData);
  };

  const handleHideMobileFilters = () => {
    setShowMobileFilters(false);
  };
  const handleToggleMobileFilters = () => {
    setShowMobileFilters((prev) => !prev);
  };

  return (
    <StyledStackWrapper>
      <FiltersWrapper>
        <MobFiltersWrapper>
          <TuneIcon onClick={handleToggleMobileFilters} />
          <Button onClick={() => handleCreateModalOpen(true)}>{t('button.createPoll')}</Button>
        </MobFiltersWrapper>
        <MobileFiltersWrapper show={showMobileFilters}>
          <AnimatePresence>
            {showMobileFilters && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <MobFiltersContent>
                  <TextField
                    label="Поиск"
                    name="name"
                    variant="outlined"
                    fullWidth
                    InputLabelProps={{ shrink: true }}
                    placeholder="Введите название"
                    onChange={handleFilterChange}
                  />
                  {appFilterOptions.map((filter) => (
                    <FilterSelect
                      key={filter.name}
                      label={filter.label}
                      name={filter.name}
                      value={filters[filter.name]}
                      options={filter.options}
                      onChange={handleFilterChange}
                    />
                  ))}
                </MobFiltersContent>
              </motion.div>
            )}
          </AnimatePresence>
        </MobileFiltersWrapper>
      </FiltersWrapper>
      <StyledStack>
        <TextField
          label="Поиск"
          name="name"
          variant="outlined"
          InputLabelProps={{
            shrink: true,
          }}
          placeholder="Введите название"
          onChange={handleFilterChange}
        />
        {appFilterOptions.map((filter) => (
          <FilterSelect
            key={filter.name}
            label={filter.label}
            name={filter.name}
            value={filters[filter.name]}
            options={filter.options}
            onChange={handleFilterChange}
          />
        ))}
        <PrimaryButton
          handleClick={() => handleCreateModalOpen(true)}
          caption="Создать опрос"
          disabled={userData.role === 'Пользователь'}
        />
      </StyledStack>
    </StyledStackWrapper>
  );
};

export default AppPollFilters;
