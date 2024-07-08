import { MenuItem, TextField } from '@mui/material';

const FilterSelect = ({ label, name, value, options, onChange }) => {
  return (
    <TextField
      select
      label={label}
      variant="outlined"
      name={name}
      value={value}
      onChange={onChange}
      fullWidth
      style={{ minWidth: '120px' }}
    >
      {options.map((option) => (
        <MenuItem key={option.value} value={option.value}>
          {option.label}
        </MenuItem>
      ))}
    </TextField>
  );
};

export default FilterSelect;
