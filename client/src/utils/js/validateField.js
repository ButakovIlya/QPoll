export const validateField = (value, pattern, errorMessage) => {
  if (!pattern.test(value)) {
    return errorMessage;
  }
  return '';
};
