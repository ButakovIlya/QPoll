import { Workbook } from 'exceljs';

import { DownloadBtn } from './styled';

const GenExcelResults = ({ data, questions }) => {
  console.log(data);
  const answers = data?.answers ?? [];

  const getQuestionAnswers = (questionId) => {
    return answers
      .map((answer) => {
        const relevantAnswers = answer.answers.filter((a) => a.answers.question === questionId);
        return relevantAnswers.length > 0
          ? { profile: answer.profile, voting_date: answer.voting_date, answers: relevantAnswers }
          : null;
      })
      .filter((item) => item !== null);
  };

  const formatDate = (dateString) => {
    if (!dateString) {
      return 'Дата не указана';
    }

    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');

    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
  };

  const downloadExcel = async () => {
    const workbook = new Workbook();
    const worksheet = workbook.addWorksheet('My Sheet');

    const questionsNames = questions?.map((question) => question.name);
    const headers = [
      'ФИО',
      'Номер студенческого',
      'Номер группы',
      'Дата голосования',
      ...questionsNames,
    ];

    worksheet.addRow(headers);

    answers.forEach((answer) => {
      const row = [];
      row.push(`${answer.profile.surname} ${answer.profile.name} ${answer.profile.patronymic}`);
      row.push(answer.profile.student_id);
      row.push(answer.profile.group);
      row.push(formatDate(answer.voting_date));

      questions.forEach((question) => {
        const questionAnswer = answer.answers.filter((a) => a.answers.question === question.id);
        console.log(questionAnswer);
        const answerText =
          questionAnswer.length > 0
            ? questionAnswer
                .map((qa) => {
                  if (qa.answers.text) {
                    return `${qa.answers.text} (Свободный ответ)`;
                  } else {
                    return qa.answers.answer_option || '';
                  }
                })
                .join(', ')
            : '';
        row.push(answerText);
      });

      worksheet.addRow(row);
    });

    headers.forEach((header, index) => {
      worksheet.getColumn(index + 1).width = header.length + 5;
    });

    const buffer = await workbook.xlsx.writeBuffer();
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'example.xlsx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <DownloadBtn onClick={downloadExcel}>Выгрузить в Excel</DownloadBtn>
    </div>
  );
};

export default GenExcelResults;
