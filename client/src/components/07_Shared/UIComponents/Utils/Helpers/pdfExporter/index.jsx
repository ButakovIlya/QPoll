import { PDFDownloadLink } from '@react-pdf/renderer';
import { useTranslation } from 'react-i18next';

const PdfExporter = ({ document, fileName }) => {
  const { t } = useTranslation();

  return (
    <PDFDownloadLink
      document={document}
      fileName={fileName}
      style={{ textDecoration: 'none', padding: '10px', color: '#4a4a4a' }}
    >
      {({ loading }) => (loading ? t('button.prepareDoc') : t('button.downloadPDF'))}
    </PDFDownloadLink>
  );
};

export default PdfExporter;
