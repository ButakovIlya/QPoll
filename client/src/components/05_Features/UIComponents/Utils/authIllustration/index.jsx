import AuthIllustrationImage from '@assets/loginIllustration.svg';
import { Link } from 'react-router-dom';

import { IllustrationGridWrapper } from './styled';

const AuthIllustration = () => {
  return (
    <IllustrationGridWrapper item>
      <Link to="/">QPoll</Link>
      <img src={AuthIllustrationImage} alt="Illustration" />
    </IllustrationGridWrapper>
  );
};

export default AuthIllustration;
