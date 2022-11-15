from django.db import models

QUESTIONS = [
    {
        'idx': question_idx,
        'title': f'Question {question_idx}',
        'text': f'Text of question {question_idx}',
        'answers_number': question_idx + 1,
        'tags': ["C++", "Python"],
    }for question_idx in range(1, 10)
]

ANSWERS = [
    {
        'text': [f'Answer {question_idx}' for i in range(30)],
    }for question_idx in range(1, 20)
]
