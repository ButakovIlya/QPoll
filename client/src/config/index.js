import packageJson from '../../package.json';

const config = {
  siteName: packageJson.name,
  imageApiUrl: import.meta.env.VITE_BASE_URL,
  serverUrl: {
    main: import.meta.env.VITE_BASE_URL,
    wsMain: import.meta.env.VITE_BASE_WS_URL,
  },
  serverPlacementsUrl: `${import.meta.env.VITE_BASE_URL}/lk_api/files/placements/`,
};
export default config;
