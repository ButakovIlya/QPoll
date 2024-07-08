import { TextField, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import ReactInputMask from 'react-input-mask';

import { StyledPasswordWrapper } from './styled';

const LabeledInput = ({
  label = '',
  required = true,
  autoComplete = '',
  id = '',
  placeholder = '',
  mask = null,
  value,
  handleChange,
  children,
  errorMessage = '',
}) => {
  const [error, setError] = useState(!!errorMessage);

  useEffect(() => {
    setError(!!errorMessage);
  }, [errorMessage]);

  return (
    <>
      <StyledPasswordWrapper>
        <Typography variant="subtitle1" gutterBottom>
          {label}
        </Typography>
        {children}
      </StyledPasswordWrapper>
      {mask ? (
        <ReactInputMask
          mask={mask}
          maskChar="_"
          value={value}
          onChange={(e) => handleChange({ target: { id, value: e.target.value } })}
        >
          {(inputProps) => (
            <TextField
              {...inputProps}
              variant="outlined"
              margin="normal"
              required={required}
              fullWidth
              id={id}
              name={id}
              autoComplete={autoComplete}
              autoFocus
              error={error}
              helperText={error ? errorMessage : ''}
              placeholder={placeholder}
            />
          )}
        </ReactInputMask>
      ) : (
        <TextField
          variant="outlined"
          margin="normal"
          required={required}
          fullWidth
          id={id}
          name={id}
          autoComplete={autoComplete}
          autoFocus
          error={error}
          value={value}
          type={id}
          onChange={handleChange}
          helperText={error ? errorMessage : ''}
          placeholder={placeholder}
        />
      )}
    </>
  );
};

export default LabeledInput;
