import { format, parseISO } from 'date-fns';

export const formatISODateTime = (isoString) => {
  const date = parseISO(isoString);
  return format(date, 'dd.MM.yyyy HH:mm');
};

export const parseAndFormatDate = (dateString) => {
  const parts = dateString.split('-');

  if (parts.length === 3) {
    const formattedDate = `${parts[2]}.${parts[1]}.${parts[0]}`;
    return formattedDate;
  } else {
    return dateString;
  }
};

export const formatDateTime = (isoString) => {
  const date = new Date(isoString);

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();

  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}.${month}.${year} ${hours}:${minutes}`;
};
