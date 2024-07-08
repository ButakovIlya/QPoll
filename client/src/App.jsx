import AppPageRoutes from '@routes/AppPageRoutes';
import { PrivateRoute } from '@routes/PrivateRoute';
import { useUnit } from 'effector-react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import { $isMaintenanceMode } from './api/store/maintenance-status';
import AdminPrivateRoute from './app/Routes/AdminPrivateRoute';
import AdminPanelPage from './components/03_Pages/Admin';
import MaintenancePage from './components/03_Pages/Maintenance';
import NotFoundPage from './components/03_Pages/NotFound';
import ConductionPollPage from './components/03_Pages/Polls/ConductionPoll';
import FastConductionPollPage from './components/03_Pages/Polls/FastConductionPoll';

import AuthPage from '@/components/03_Pages/Auth';
import HomePage from '@/components/03_Pages/Home';
import PollListPage from '@/components/03_Pages/Polls/PollList';
import FrmRestore from '@/components/04_Widgets/Data/Forms/frmRestore';

const App = () => {
  const isMaintenanceMode = useUnit($isMaintenanceMode);

  return (
    <Router>
      <Routes>
        {isMaintenanceMode ? (
          <>
            <Route path="/maintenance" element={<MaintenancePage />} />
            <Route path="*" element={<Navigate to="/maintenance" />} />
          </>
        ) : (
          <>
            <Route path="/" element={<HomePage />} />
            <Route path="/polls" element={<PollListPage />} />
            <Route path="/conduct-poll/:id" element={<ConductionPollPage />} />
            <Route path="/quick-conduct-poll/:id" element={<FastConductionPollPage />} />
            <Route path="/signin" element={<AuthPage />} />
            <Route path="/signup" element={<AuthPage />} />
            <Route path="/password-reset" element={<FrmRestore />} />
            <Route element={<PrivateRoute />}>
              <Route element={<AdminPrivateRoute />}>
                <Route path="/admin-panel/*" element={<AdminPanelPage />} />
              </Route>
              <Route path="/app/*" element={<AppPageRoutes />} />
            </Route>
            <Route path="/maintenance" element={<Navigate to="/" />} />
            <Route path="/not-found" element={<NotFoundPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </>
        )}
      </Routes>
    </Router>
  );
};

export default App;
