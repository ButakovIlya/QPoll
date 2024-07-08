import { LabeledFieldWrapper, StyledInput, StyledLabelTypography } from './styled';

const InvisibleLabeledField = ({
  label,
  placeholder,
  handleChange = () => {},
  value,
  type,
  max,
  min,
  step,
  defaultValue,
  disabled,
}) => {
  return (
    <LabeledFieldWrapper>
      <StyledLabelTypography>{label}</StyledLabelTypography>
      <StyledInput
        disabled={disabled}
        id={type}
        fullWidth
        placeholder={placeholder}
        onChange={(e) => handleChange(e.target.value)}
        value={value}
        type={type}
        step={step}
        defaultValue={defaultValue}
        inputProps={{ max: max, min: min }}
      />
    </LabeledFieldWrapper>
  );
};

export default InvisibleLabeledField;
