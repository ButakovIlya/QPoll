import { v4 } from 'uuid';

import { CardsWrapper, PollListGridContainer } from './styled';

import { regOnPollFx } from '@/api/common-requests/poll-register';
import AppPoleCard from '@/components/04_Widgets/Data/Cards/appPoleCard';
import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';

const PollListOut = ({ polls = [] }) => {
  const handleRegistration = async (poll_id) => {
    await regOnPollFx({ poll_id });
  };

  return (
    <PollListGridContainer>
      {polls.map((item) => (
        <CardsWrapper key={v4()} item xs={12} sm={6}>
          <AppPoleCard
            pollData={item}
            cardButton={
              item.has_user_participated_in && !item.is_revote_allowed ? (
                !item.opened_for_voting ? (
                  <PrimaryButton
                    caption="Зарегистрироваться"
                    handleClick={() => handleRegistration(item.poll_id)}
                    style={{ border: '1px solid orange', color: 'orange' }}
                  />
                ) : (
                  <PrimaryButton caption="Пройден" disabled={true} />
                )
              ) : (
                <PrimaryButton
                  caption="Пройти"
                  to={`/${item.poll_type.name === 'Быстрый' ? 'quick-conduct-poll' : 'conduct-poll'}/${item.poll_id}`}
                />
              )
            }
          />
        </CardsWrapper>
      ))}
    </PollListGridContainer>
  );
};

export default PollListOut;
