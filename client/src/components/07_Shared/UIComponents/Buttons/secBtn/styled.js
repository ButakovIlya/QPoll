import styled from '@emotion/styled';
import { Rem } from '@/utils/convertToRem';
import { designTokens } from '@/constants/designTokens';
import { colorConfig } from '@/app/template/config/color.config';

export const StyledButton = styled('button')(() => ({
  fontSize: Rem(16),
  backgroundColor: colorConfig.primaryBlue,
  color: '#fff',
  border: 'none',
  padding: `${Rem(16)} ${Rem(30)}`,
  borderRadius: designTokens.borderRadius.buttonBorder,
  cursor: 'pointer',
}));
