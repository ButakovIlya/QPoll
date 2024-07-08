import config from '@config';

export const API_URL = {
  MAIN: `${config.serverUrl.main}/`,
  // IMAGE: `${config.imageApiUrl}/`,
};

export const ENDPOINTS = {
  USER: {
    GET_SELF: `lk_api/user/`,
    REGISTRATION: `lk_api/register`,
    LOGIN: `lk_api/login`,
    TOKEN_REFRESH: `lk_api/refresh`,
    PASSWORD_RESET: `lk_api/reset-password`,
    CREATE_PASSWORD: `lk_api/create-password`,
    REQUEST_CODE: `lk_api/register/request-code`,
    CONFIRM_CODE: `lk_api/register/confirm-code`,
  },
  //   CAMPAIGNS: {
  //     GET_CAMPAIGNS: `lk_api/campaigns/`,
  //     CREATE_CAMPAIGN_OF_SITE: `lk_api/campaigns/`,
  //     GET_SINGLE_CAMPAIGN: (campaign_id) => `/lk_api/campaigns/${campaign_id}`,
  //     DELETE_SINGLE_CAMPAIGN: (campaign_id) => `lk_api/campaigns/${campaign_id}`,
  //   },
  //   SPACES: {
  //     GET_SPACES_GROUPED_BY_SITES: `/lk_api/spaces/grouped_by_sites`,
  //     GET_SPACE: (space_id) => `/lk_api/spaces/${space_id}`,
  //     CREATE_SPACE: `/lk_api/spaces/`,
  //     UPDATE_SPACE: (space_id) => `/lk_api/spaces/${space_id}`,
  //     TEST_CODE: (space_id) => `/lk_api/spaces/${space_id}/test_code`,
  //   },
  //   ADS: {
  //     GET_CAMPAIGN_ADS: ({ site_id, campaign_id }) =>
  //       `lk_api/sites/${site_id}/campaigns/${campaign_id}/ads/`,
  //   },
  //   STATS: {
  //     BY_DATE: `lk_api/stats/by_date`,
  //     BY_DATE_MULTISELECT: `lk_api/stats/by_date_multiselect`,
  //     BY_CAMPAIGNS: `lk_api/stats/by_campaigns`,
  //     BY_SITES: `lk_api/stats/by_sites`,
  //     BY_CAMPAIGNS_IN_SITES: `lk_api/stats/by_campaigns_in_sites`,
  //   },
};
