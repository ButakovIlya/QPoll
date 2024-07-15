from .exсeptions import *
from .serializers import PollAnswerGroupSerializer, PollParticipantsGroupSerializer
from .models import PollAnswer

from datetime import datetime
from .utils import PollVoting
# from qpoll.settings import w3, contract

def poll_voting_handler(answers, poll, is_full=True):
    raw_answers = answers
    required_questions = {question for question in poll.questions.all() if question.is_required}
    answered_questions = set()

    parsed_answers = []
    
    questions_with_answer_options = poll.questions.all()
    
    for answer in answers:
        question_id = answer.get('question', None)
        if not question_id:
            raise MissingFieldException(field_name='question')
        
        answer_option_id = answer.get('answer_option', None)
        if not answer_option_id:
            raise MissingFieldException(field_name='answer_option')

        question = next((q for q in questions_with_answer_options if q.id == question_id), None)
        
        if not question:
            raise ObjectNotFoundException(model='PollQuestion')
              
        if isinstance(answer_option_id, list):
            answer_option_ids = answer_option_id
            
            if not question.has_multiple_choices:
                raise PollAnsweringException(detail=f"{question} не поддерживает множественный выбор ответов")
            else:
                answer_options = [option for option in question.answer_options.all() if option.id in answer_option_ids]
                if len(answer_options) != len(answer_option_ids):
                    raise ObjectNotFoundException(model='AnswerOption')
                    
                for answer_option in answer_options:
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option.id})
                answered_questions.add(question)
        else:
            answer_option = next((option for option in question.answer_options.all() if option.id == answer_option_id), None)
            if not answer_option:
                raise ObjectNotFoundException(model='AnswerOption')
            
            if question.is_free:
                text = answer.get('text', None)
                if not text:
                    raise PollAnsweringException(detail=f"Вопрос с открытым ответом должен содержать текст ответа")
                parsed_answers.append({'question': question_id, 'answer_option': answer_option_id, 'text': text})
            else:
                if answer_option.is_free_response: # проверяем что вариант ответа содержит свободную форму ответа
                    text = answer.get('text', None)
                    if not text:
                        raise PollAnsweringException(detail=f"Поле со свободным ответом должно содержать текст ответа")
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option_id, 'text': text})
                else:
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option_id})
            
            # добавляем в список отвеченных вопросов
            answered_questions.add(question)

    if is_full:
        if not required_questions.issubset(answered_questions):
            difference = list(required_questions.difference(answered_questions))
            raise PollAnsweringException(detail=f"Вы ответили не на все обязательные вопросы: {difference}")

    return parsed_answers, raw_answers


def quizz_voting_handler(answers, poll, is_full=True):
    required_questions = {question for question in poll.questions.all() if question.is_required}
    answered_questions = set()

    parsed_answers = []
    
    questions_with_answer_options = poll.questions.all()
    
    for answer in answers:
        question_id = answer.get('question', None)
        if not question_id:
            raise MissingFieldException(field_name='question')
        
        answer_option_id = answer.get('answer_option', None)
        if not answer_option_id:
            raise MissingFieldException(field_name='answer_option')

        question = next((q for q in questions_with_answer_options if q.id == question_id), None)
        
        if not question:
            raise ObjectNotFoundException(model='PollQuestion')
              
        if isinstance(answer_option_id, list):
            answer_option_ids = answer_option_id
            
            if not question.has_multiple_choices:
                raise PollAnsweringException(detail=f"{question} не поддерживает множественный выбор ответов")
            else:
                answer_options = [option for option in question.answer_options.all() if option.id in answer_option_ids]
                if len(answer_options) != len(answer_option_ids):
                    raise ObjectNotFoundException(model='AnswerOption')
                    
                for answer_option in answer_options:
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option.id})
                answered_questions.add(question)
        else:
            answer_option = next((option for option in question.answer_options.all() if option.id == answer_option_id), None)
            if not answer_option:
                raise ObjectNotFoundException(model='AnswerOption')
            
            if question.is_free:
                text = answer.get('text', None)
                if not text:
                    raise PollAnsweringException(detail=f"Вопрос с открытым ответом должен содержать текст ответа")
                parsed_answers.append({'question': question_id, 'answer_option': answer_option_id, 'text': text})
            else:
                if answer_option.is_free_response: # проверяем что вариант ответа содержит свободную форму ответа
                    text = answer.get('text', None)
                    if not text:
                        raise PollAnsweringException(detail=f"Поле со свободным ответом должно содержать текст ответа")
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option_id, 'text': text})
                else:
                    parsed_answers.append({'question': question_id, 'answer_option': answer_option_id})
            
            # добавляем в список отвеченных вопросов
            answered_questions.add(question)

    if is_full:
        if not required_questions.issubset(answered_questions):
            difference = list(required_questions.difference(answered_questions))
            raise PollAnsweringException(detail=f"Вы ответили не на все обязательные вопросы: {difference}")

    return parsed_answers


def save_votes(answers, poll, my_profile, raw_answers,
               poll_answer_group=None, poll_participation_group=None, quick_voting_form=None):
    if not poll_answer_group:
        poll_answer_group_data = {
                    'poll': poll.id,
                    'is_finished':True,
                    'voting_end_date': datetime.now()
        }
        
        if not poll.poll_type.name in ('Анонимный', 'Быстрый'):
            poll_answer_group_data['profile'] = my_profile.user_id
        if poll.poll_type.name in ('Быстрый'):
            poll_answer_group_data['quick_voting_form'] = quick_voting_form.id

        poll_answer_group = PollAnswerGroupSerializer(data=poll_answer_group_data)
        if poll_answer_group.is_valid():
            poll_answer_group = poll_answer_group.save()
        else:
            raise MyCustomException(detail=poll_answer_group.errors)
    else:
        poll_answer_group = poll_answer_group

    if not poll_participation_group:
        poll_participation_group_data = {
                'poll': poll.id,
                'is_latest': True,
            }

        if not poll.poll_type.name in ("Быстрый"):
            poll_participation_group_data['profile'] = my_profile.user_id
            poll_participation_group_data['quick_voting_form'] = None
        else:
            poll_participation_group_data['quick_voting_form'] = quick_voting_form.id
            poll_participation_group_data['profile'] = None

        poll_participation_group = PollParticipantsGroupSerializer(data=poll_participation_group_data)
        if poll_participation_group.is_valid():
            poll_participation_group = poll_participation_group.save()
        else:
            raise MyCustomException(detail=poll_participation_group.errors)

    data = answers
    # Получите все вопросы в один запрос
    poll_questions = poll.questions.all()
    questions_dict = {question.id: question for question in poll_questions}

    # Получите все варианты ответов в один запрос
    answer_options_dict = {
        question.id: {answer_option.id: answer_option for answer_option in question.answer_options.all()}
        for question in poll_questions
    }

    for answer in data:
        answer['poll_answer_group'] = poll_answer_group
        answer['poll'] = poll
        question_id = answer['question']
        question = questions_dict.get(question_id)
        if question:
            answer['question'] = question
            answer_option_id = answer['answer_option']
            answer_option = answer_options_dict.get(question_id, {}).get(answer_option_id)

            if poll.poll_type.name == 'Викторина':
                if question.is_free:
                    if answer_option.name.lower().rstrip() == answer['text'].lower().rstrip():
                        answer['points'] = 1
                    else:
                        answer['points'] = 0
                else:
                    if answer_option.is_free_response:
                        if answer_option.name.lower().rstrip() == answer['text'].lower().rstrip():
                            answer['points'] = 1
                        else:
                            answer['points'] = 0
                    else:
                        if answer_option.is_correct is not None:
                            if answer_option.is_correct:
                                answer['points'] = 1
                            else:
                                answer['points'] = 0

            answer['answer_option'] = answer_option

    poll_answers = PollAnswer.objects.bulk_create([
        PollAnswer(**item) for item in data
    ])

    poll_data = {
        'poll_id': poll.poll_id,
        'answers': raw_answers,
    }

    tx_hash = None
    # if poll.poll_type.name == "Анонимный":
    #     poll_answer_group_data['profile'] = None
    #     tx_hash = PollVoting(w3, contract, poll_data)

    return poll_answer_group, poll_answers, tx_hash





