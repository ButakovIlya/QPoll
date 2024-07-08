export const nameReducer = (fullName) => {
  const parts = fullName.trim().split(' ');

  if (parts.length < 3) return fullName;

  const [lastName, firstName, middleName] = parts;

  return `${lastName} ${firstName[0]}. ${middleName[0]}.`;
};
