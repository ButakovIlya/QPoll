import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { v4 } from 'uuid';

import {
  BtnsWrapper,
  CopyButton,
  LinkBox,
  LinkContent,
  LinkDesc,
  LinkField,
  LinkTitle,
  ShareBtn,
  ShareBtnContent,
  ShareDescription,
  ShareTextWrapper,
  ShareTitle,
  StyledArrowForwardIosIcon,
} from './styled';

import { colorConfig } from '@/app/template/config/color.config';
import { shareButtons } from '@/data/fields';
import usePollData from '@/hooks/usePollData';

const FrmShareMain = ({ setView }) => {
  const { id } = useParams();
  const { pollType } = usePollData(id);
  const [surveyLink, setSurveyLink] = useState('');
  const [buttonText, setButtonText] = useState('Копировать');
  const [fieldColor, setFieldColor] = useState('rgba(39,116,248,.11)');
  const [btnColor, setBtnColor] = useState(colorConfig.primaryBlue);

  useEffect(() => {
    const host = window.location.host;
    const protocol = window.location.protocol;
    const link = `${protocol}//${host}/${pollType === 'Быстрый' ? 'quick-conduct-poll' : 'conduct-poll'}/${id}`;
    setSurveyLink(link);
  }, [id, pollType]);

  const handleCopy = () => {
    navigator.clipboard.writeText(surveyLink);
    setButtonText('Скопировано');
    setFieldColor('rgba(100,255,100,.3)');
    setBtnColor('#48c855');

    setTimeout(() => {
      setButtonText('Копировать');
      setFieldColor('rgba(39,116,248,.11)');
      setBtnColor(colorConfig.primaryBlue);
    }, 1000);
  };
  return (
    <>
      <LinkContent>
        <LinkTitle>Прямая ссылка на ваш опрос</LinkTitle>
        <LinkDesc>Скопируйте и отправьте своим респондентам ссылку</LinkDesc>
        <LinkBox>
          <LinkField fullWidth value={surveyLink} propColor={fieldColor} textColor={btnColor} />
          <CopyButton onClick={() => handleCopy()} propColor={btnColor}>
            {buttonText}
          </CopyButton>
        </LinkBox>
      </LinkContent>
      <BtnsWrapper>
        {shareButtons.map((item) => (
          <ShareBtn key={v4()} onClick={() => setView(item.view)}>
            <ShareBtnContent>
              <item.icon sx={{ fontSize: '30px' }} />
              <ShareTextWrapper>
                <ShareTitle>{item.caption}</ShareTitle>
                <ShareDescription>{item.description}</ShareDescription>
              </ShareTextWrapper>
            </ShareBtnContent>
            <StyledArrowForwardIosIcon />
          </ShareBtn>
        ))}
      </BtnsWrapper>
    </>
  );
};

export default FrmShareMain;
