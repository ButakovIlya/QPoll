import i18n from 'i18next';
import { merge } from 'lodash';
import { initReactI18next } from 'react-i18next';

import ru_alert from './ru/ru.alert.json';
import ru_assits from './ru/ru.assist.json';
import ru_buttons from './ru/ru.buttons.json';
import ru_field from './ru/ru.field.json';
import ru_head from './ru/ru.head.json';
import ru_label from './ru/ru.labels.json';
import ru_nav from './ru/ru.navigation.json';

const ru_controls = merge(ru_buttons, ru_assits, ru_field, ru_nav);

const ru_translation = merge(ru_alert, ru_controls, ru_head, ru_label);

const resources = {
  en: { translation: ru_translation },
  ru: { translation: ru_translation },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'ru',
  fallbackLng: 'ru',

  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
