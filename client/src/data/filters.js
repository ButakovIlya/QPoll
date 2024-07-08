export const appTypesFilter = [
  { value: 'Все типы', label: 'Все типы' },
  { value: 'Опрос', label: 'Опрос' },
  { value: 'Викторина', label: 'Викторина' },
];

export const appStatusesFilter = [
  { value: 'Все статусы', label: 'Все статусы' },
  { value: '0', label: 'Открытые' },
  { value: '1', label: 'Закрытые' },
];

export const appGroupsFilter = [
  { value: 'Для всех', label: 'Для всех' },
  { value: 'Group 2', label: 'Group 2' },
  { value: 'Group 3', label: 'Group 3' },
];

export const appFilterOptions = [
  { label: 'Тип', name: 'poll_type', options: appTypesFilter },
  { label: 'Статус', name: 'is_closed', options: appStatusesFilter },
  { label: 'Группа', name: 'group', options: appGroupsFilter },
];

export const admUsrsFilterCategories = [
  { name: 'Сортировка по', options: ['Опция 1', 'Опция 2'] },
  { name: 'Тип опроса', options: ['Опрос 1', 'Опрос 2'] },
  { name: 'Статус', options: ['Активный', 'Неактивный'] },
  { name: 'Группа', options: ['Группа 1', 'Группа 2'] },
];
