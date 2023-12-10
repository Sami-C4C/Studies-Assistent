# quizzes/utils.py

from .models import Question


def check_answer(question_id, selected_option):
    question = Question.objects.get(pk=question_id)
    return question.correct_answer == selected_option
