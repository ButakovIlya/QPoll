import packageJson from '../../package.json';

const config = {
  siteName: packageJson.name,
  imageApiUrl: import.meta.env.VITE_BASE_URL,
  serverUrl: {
    main: '95.163.221.120:9000',
    wsMain: import.meta.env.VITE_BASE_WS_URL,
  },
  serverPlacementsUrl: `${import.meta.env.VITE_BASE_URL}/lk_api/files/placements/`,
};
export default config;
