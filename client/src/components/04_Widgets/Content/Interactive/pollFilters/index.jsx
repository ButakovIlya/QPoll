import FilterListIcon from '@mui/icons-material/FilterList';
import { FormControlLabel, TextField, Typography, useMediaQuery } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { applyFiltersFx } from './models/apply-filters';
import { FiltersButton, FiltersWrapper, StyledFormGroup } from './styled';

import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import CustomSwitch from '@/components/07_Shared/UIComponents/Buttons/switch';
import FilterSelect from '@/components/07_Shared/UIComponents/Fields/filterSelect';
import { appTypesFilter } from '@/data/filters';

const PollFilters = ({ setPolls }) => {
  const { t } = useTranslation();
  const [filters, setFilters] = useState({
    name: '',
    poll_type: '',
    is_anonymous: false,
  });
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const matches = useMediaQuery('(max-width:1000px)');

  const handleChange = (event) => {
    const { name, value, checked, type } = event.target;
    setFilters((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleApplyFilters = async () => await applyFiltersFx({ filters, setPolls });

  const toggleFilters = () => setIsFiltersOpen(!isFiltersOpen);

  return (
    <FiltersWrapper>
      {matches ? (
        <FiltersButton onClick={toggleFilters}>
          <FilterListIcon sx={{ mr: 1 }} /> Фильтры
        </FiltersButton>
      ) : (
        <Typography variant="h6">Фильтры</Typography>
      )}
      {(!matches || isFiltersOpen) && (
        <StyledFormGroup>
          <TextField
            label="Поиск"
            name="name"
            variant="outlined"
            value={filters.name}
            onChange={handleChange}
            fullWidth
            sx={{ my: 2 }}
          />
          <FilterSelect
            label="Выберите тип"
            options={appTypesFilter}
            value={filters.poll_type}
            onChange={handleChange}
            name="poll_type"
          />
          <FormControlLabel
            control={
              <CustomSwitch
                checked={filters.is_anonymous}
                onChange={handleChange}
                name="is_anonymous"
              />
            }
            label="Анонимный"
          />
          <PrimaryButton
            caption={t('button.applyFilters')}
            handleClick={handleApplyFilters}
            style={{ marginTop: '5px' }}
          />
        </StyledFormGroup>
      )}
    </FiltersWrapper>
  );
};

export default PollFilters;
