import BlockIcon from '@mui/icons-material/Block';
import GroupAddIcon from '@mui/icons-material/GroupAdd';
import SettingsIcon from '@mui/icons-material/Settings';
import { useEffect, useState } from 'react';

import { banUserFx } from './models/ban-user';
import { getAllUsersFx } from './models/get-users';

import { roleColorsConf } from '@/app/template/config/role.colors';
import AdmUsrFilters from '@/components/04_Widgets/Content/Interactive/admUsrFilters';
import FrmAdmUserSettings from '@/components/04_Widgets/Data/Forms/frmAdmUserSettings';
import CustomTable from '@/components/04_Widgets/Data/Vizualization/table';
import FrmConfirm from '@/components/04_Widgets/Utilities/Modals/frmConfirm';
import { parseAndFormatDate } from '@/utils/js/formatDate';

const AdminUsersPage = () => {
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [userIdToBlock, setUserIdToBlock] = useState(null);
  const [userIdToChange, setUserIdToChange] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchAllUsers = async () => {
      const usersResponse = await getAllUsersFx();
      setUsers(usersResponse.data.results);
    };
    fetchAllUsers();
  }, []);

  const handleOpenConfirm = (userId, status) => {
    setIsConfirmOpen(true);
    setUserIdToBlock({ id: userId, status });
  };

  const handleBlockUser = async () => {
    try {
      const updatedUser = await banUserFx({ id: userIdToBlock.id, status: userIdToBlock.status });
      setUsers((prevUsers) =>
        prevUsers.map((user) => (user.user.id === userIdToBlock.id ? updatedUser : user)),
      );
      setIsConfirmOpen(false);
      setUserIdToBlock(null);
    } catch (error) {
      console.error('Ошибка при бане пользователя:', error);
    }
  };

  const handleChangeStatus = (userId) => {
    setUserIdToChange(userId);
    setIsSettingsOpen(true);
  };

  const getAdminUsersTableColumns = (handleChangeStatus) => [
    { id: 1, key: 'id', caption: 'ID', render: (_, user) => (user.user.id ? user.user.id : '-') },
    { id: 2, key: 'name', caption: 'Имя', render: (name) => name ?? '-' },
    { id: 3, key: 'email', caption: 'Email' },
    {
      id: 4,
      key: 'joining_date',
      caption: 'Дата вступления',
      render: (joining_date) => parseAndFormatDate(joining_date),
    },
    {
      id: 5,
      key: 'role',
      caption: 'Роль',
      render: (role) => <span style={{ color: roleColorsConf[role] }}>{role}</span> ?? '-',
    },
    {
      id: 6,
      key: 'is_banned',
      caption: 'Статус',
      render: (isBanned) => (
        <span
          style={{
            color: isBanned ? '#EF3826' : '#00B69B',
            backgroundColor: isBanned ? 'rgba(239, 56, 38, .2)' : 'rgba(0, 182, 155, .3)',
            padding: '6px 16px',
            borderRadius: '5px',
            fontWeight: 500,
          }}
        >
          {isBanned ? 'Заблокирован' : 'Активен'}
        </span>
      ),
    },
    {
      id: 7,
      key: 'actions',
      caption: 'Действия',
      render: (_, user) => (
        <>
          {!user.is_banned ? (
            <BlockIcon
              onClick={() => handleOpenConfirm(user.user.id, 1)}
              color="error"
              sx={{ cursor: 'pointer' }}
            />
          ) : (
            <GroupAddIcon
              onClick={() => handleOpenConfirm(user.user.id, 0)}
              color="success"
              sx={{ cursor: 'pointer' }}
            />
          )}
          <SettingsIcon
            onClick={() => handleChangeStatus(user.user.id)}
            sx={{ ml: 1, cursor: 'pointer' }}
          />
        </>
      ),
    },
  ];

  return (
    <>
      <AdmUsrFilters />
      <CustomTable columns={getAdminUsersTableColumns(handleChangeStatus)} data={users} />
      <FrmAdmUserSettings
        open={isSettingsOpen}
        handleClose={setIsSettingsOpen}
        userId={userIdToChange}
        setUsers={setUsers}
      />
      <FrmConfirm
        open={isConfirmOpen}
        onCancel={() => setIsConfirmOpen(false)}
        onConfirm={() => handleBlockUser()}
      />
    </>
  );
};

export default AdminUsersPage;
