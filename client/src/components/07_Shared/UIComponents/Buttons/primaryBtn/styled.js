import styled from '@emotion/styled';

import { colorConfig } from '@/app/template/config/color.config';
import { designTokens } from '@/constants/designTokens';
import { Rem } from '@/utils/convertToRem';

export const StyledButton = styled('button')(({ disabled }) => ({
  fontSize: Rem(16),
  backgroundColor: 'transparent',
  color: !disabled ? colorConfig.primaryBlue : '#aaa',
  border: `${Rem(1)} solid ${!disabled ? colorConfig.primaryBlue : '#aaa'}`,
  padding: `${Rem(10)} ${Rem(24)}`,
  borderRadius: designTokens.borderRadius.buttonBorder,
  cursor: !disabled ? 'pointer' : 'not-allowed',
  '@media (max-width: 1100px)': {
    fontSize: Rem(13),
    padding: `${Rem(6)} ${Rem(16)}`,
  },
}));
