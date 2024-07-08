import ResultsIcon from '@mui/icons-material/BarChart';
import QuestionsIcon from '@mui/icons-material/HelpOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import IntegrationIcon from '@mui/icons-material/SettingsEthernet';

import PoleMainSettingsPage from '../../Pole/PoleMainSettings';
import PoleQuestionsPage from '../../Pole/PoleQuestions';
import PollResultsPage from '../../Pole/PollResults';

export const poleNavigationButtonsData = [
  {
    icon: SettingsIcon,
    label: 'Основное',
    page: 'main',
    component: PoleMainSettingsPage,
  },
  {
    icon: ResultsIcon,
    label: 'Результаты',
    page: 'results',
    component: PollResultsPage,
    disabled: false,
  },
  { icon: QuestionsIcon, label: 'Вопросы', page: 'questions', component: PoleQuestionsPage },
  {
    icon: IntegrationIcon,
    label: 'Интеграции',
    page: 'integrations',
    component: '4',
    disabled: true,
  },
];
