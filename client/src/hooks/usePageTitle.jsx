import config from '@config';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const usePageTitle = (titleLocale) => {
  const { t } = useTranslation();

  const prepared = titleLocale ? t(`head.title.${titleLocale}`) : '';

  const pageTitle = config.siteName ? config.siteName + ' - ' + prepared : 'QPoll';
  useEffect(() => {
    document.title = pageTitle;
  }, [pageTitle]);
  return pageTitle;
};
export default usePageTitle;
