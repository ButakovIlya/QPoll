import { IOSSwitch } from './styled';

const CustomSwitch = ({
  focusVisibleClassName,
  onChange = () => {},
  checked = false,
  name = '',
  disabled,
}) => {
  return (
    <IOSSwitch
      disabled={disabled}
      focusVisibleClassName={focusVisibleClassName}
      disableRipple
      onChange={onChange}
      sx={{ m: 1 }}
      checked={checked}
      name={name}
    />
  );
};

export default CustomSwitch;
