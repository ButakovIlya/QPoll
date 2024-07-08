import { Document, Font, Page, StyleSheet, Text, View } from '@react-pdf/renderer';
import { useEffect, useState } from 'react';

Font.register({
  family: 'Roboto',
  src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-medium-webfont.ttf',
});

const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#fff',
    padding: 30,
    fontFamily: 'Roboto',
    fontSize: 14,
  },
  header: {
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 6,
  },
  subtitle: {
    marginBottom: 20,
    textAlign: 'center',
  },
  answerTable: {
    marginBottom: 20,
  },
  tableRow: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    paddingVertical: 8,
  },
  tableHeader: {
    backgroundColor: '#f0f0f0',
  },
  tableCol: {
    flex: 1,
    paddingHorizontal: 5,
  },
});

const PollResultsPDF = ({ data, pollData }) => {
  const [currentDate, setCurrentDate] = useState('');
  const questions = data?.poll_data?.questions ?? [];
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

  useEffect(() => {
    const currentISODate = new Date().toISOString().slice(0, 16);
    setCurrentDate(currentISODate);
  }, []);

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <Text style={styles.header}>Результаты опроса: {pollData.name}</Text>
        <Text style={styles.subtitle}>
          Результаты экспортированы: {currentDate}
          {'\n'}Тип опроса: {pollData.poll_type.name}
        </Text>
        <Text style={styles.infoText}>
          Автор опроса: {pollData.author.surname} {pollData.author.name}
        </Text>
        <Text style={styles.infoText}>Описание: {pollData.description ?? '-'}</Text>
        <Text style={styles.infoText}>Дата начала: {pollData.poll_setts.start_time ?? '-'}</Text>
        <Text style={styles.infoText}>Дата окончания: {pollData.poll_setts.end_time ?? '-'}</Text>
        <Text style={styles.infoText}>
          Длительность прохождения: {pollData.poll_setts.completion_time ?? '-'}
        </Text>
        <Text style={styles.infoText}>Количество вопросов: {pollData.questions_quantity}</Text>
        <Text style={styles.infoText}>Количество участников: {pollData.participants_quantity}</Text>
        <Text style={styles.infoText}>
          Защита от списывания: {pollData.mix_options || pollData.mix_questions ? 'Да' : 'Нет'}
        </Text>
        {questions.map((question, index) => {
          const questionAnswers = getQuestionAnswers(question.id);
          return (
            <View key={index}>
              <Text style={styles.questionTitle}>{`Вопрос ${index + 1}: ${question.name}`}</Text>

              <View style={styles.answerTable}>
                <View style={[styles.tableRow, styles.tableHeader]}>
                  <Text style={styles.tableCol}>ФИО</Text>
                  <Text style={styles.tableCol}>Вариант ответа</Text>
                  <Text style={styles.tableCol}>Дата ответа</Text>
                </View>

                {questionAnswers.map((answer, idx) => (
                  <View key={idx}>
                    {answer.answers.length > 1 ? (
                      <View style={styles.tableRow}>
                        <Text
                          style={styles.tableCol}
                        >{`${answer?.profile?.surname} ${answer?.profile?.name}`}</Text>
                        <Text style={styles.tableCol}>
                          {answer.answers
                            .map((a) =>
                              a.answers.text
                                ? `${a.answers.text}(Свободный ответ)`
                                : a.answers.answer_option,
                            )
                            .join(', ')}{' '}
                        </Text>
                        <Text style={styles.tableCol}>{answer.voting_date}</Text>
                      </View>
                    ) : (
                      answer.answers.map((a, aIdx) => (
                        <View key={`${idx}-${aIdx}`} style={styles.tableRow}>
                          <Text
                            style={styles.tableCol}
                          >{`${answer?.profile?.surname} ${answer?.profile?.name}`}</Text>
                          <Text style={styles.tableCol}>
                            {a.answers.text
                              ? `${a.answers.text}(Свободный ответ)`
                              : a.answers.answer_option}
                          </Text>
                          <Text style={styles.tableCol}>{answer.voting_date}</Text>
                        </View>
                      ))
                    )}
                  </View>
                ))}
              </View>
            </View>
          );
        })}
      </Page>
    </Document>
  );
};

export default PollResultsPDF;
