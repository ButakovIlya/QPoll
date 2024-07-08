import MiniPollABI from '@config/ABI.json';
import { createEffect } from 'effector';
import Web3 from 'web3';

const ganacheUrl = 'http://81.200.154.220:8545';

export const sendAnonymousAnswersFx = createEffect(async ({ answers, id, isTimeEnd }) => {
  const web3 = new Web3(ganacheUrl);

  const miniPollContract = new web3.eth.Contract(
    MiniPollABI.abi,
    '0x3cd53c52de7e9919c3969f0ea73732b01af7611c',
  );

  const voteHashes = answers.map((answer) =>
    web3.utils.soliditySha3(answer.question, answer.answer_option),
  );

  const accounts = await web3.eth.getAccounts();

  console.log(voteHashes);
  miniPollContract.methods
    .vote(id, voteHashes)
    .send({ from: accounts[0], gas: '1000000', gasPrice: 1000000000 })
    .then((receipt) => {
      console.log('Голоса пользователя успешно отправлены.');
    })
    .catch((error) => {
      console.error('Ошибка при отправке голосов пользователя:', error);
    });
  const allVotes = await miniPollContract.methods.getPollResponses(id).call();
  const decodedVotes = allVotes.map((vote) => {
    return web3.utils.hexToAscii(vote);
  });
  console.log('Все голоса для ID:', id, decodedVotes);
});
