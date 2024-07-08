import { AlertProvider } from '@app/context/AlertProvider';
import { AuthProvider } from '@app/context/AuthProvider';
import ReactDOM from 'react-dom/client';

import 'core-js/stable';
import 'regenerator-runtime/runtime';
import './app/template/__init__.css';

import '@locale/i18n';
import App from './App';
import { UserRoleProvider } from './app/context/UserRoleProvider';
import AlertPopup from './components/04_Widgets/Utilities/Modals/alert';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AlertProvider>
    <AuthProvider>
      <UserRoleProvider>
        <AlertPopup />
        <App />
      </UserRoleProvider>
    </AuthProvider>
  </AlertProvider>,
);
