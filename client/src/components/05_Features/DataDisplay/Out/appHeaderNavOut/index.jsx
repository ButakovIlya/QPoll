import { v4 } from 'uuid';

import { StyledNavLink, StyledNavigation, StyledNavigationList } from './styled';

const AppHeaderNavOut = ({ itemsData = [] }) => {
  return (
    <StyledNavigation>
      <StyledNavigationList>
        {itemsData.map((item) => {
          return (
            <StyledNavLink
              end
              key={v4()}
              to={item.to}
              className={({ isActive, isPending }) =>
                isPending ? 'pending' : isActive ? 'active' : ''
              }
            >
              {item.caption}
            </StyledNavLink>
          );
        })}
      </StyledNavigationList>
    </StyledNavigation>
  );
};

export default AppHeaderNavOut;
