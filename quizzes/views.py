# quizzes/views.py
import os
import string

import openai
from django.shortcuts import get_object_or_404


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Quiz, Question, UserAnswer, Option


# Stellen Sie sicher, dass Sie Ihren API-Schlüssel korrekt einrichten
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)
MODEL = "gpt-3.5-turbo"


def index_view(request):
    return render(request, 'quizzes/index.html')


def tools_view(request):
    return render(request, 'quizzes/tools.html')


def guidelines_view(request):
    return render(request, 'quizzes/guidelines.html')


def tipps_view(request):
    return render(request, 'quizzes/tipps.html')


def helfer_view(request):
    return render(request, 'quizzes/KI-Helfer.html')


def assistent_view(request):
    return render(request, 'quizzes/assistent.html')


def generate_quiz(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        generated_data = generate_quiz_content(category, 5, 4)

        if generated_data:
            quiz = Quiz.objects.create(category=category)
            for item in generated_data:
                question_text = item['question_text']
                question = Question.objects.create(quiz=quiz, text=question_text)
                for i, option_text in enumerate(item['options']):
                    is_correct = (i == item['correct_option_index'])
                    Option.objects.create(question=question, text=option_text, is_correct=is_correct)
            # Fetch the questions again along with their options to pass to the template
            questions_with_options = Question.objects.filter(quiz=quiz).prefetch_related('choices')
            return render(request, 'quizzes/generated_quiz.html', {
                'quiz': quiz,
                'questions': questions_with_options,
                'category': category
            })
        else:
            # Handle the case when no questions are generated
            return render(request, 'quizzes/generated_quiz.html', {
                'error': 'Es wurden keine Fragen generiert.',
                'category': category
            })

    return render(request, 'quizzes/assistent.html')


def generate_options(num_options):
    options = []
    alphabet = string.ascii_uppercase
    for i in range(num_options):
        option = alphabet[i]
        options.append(option)
    return options


def generate_quiz_content(category, num_questions, num_options):
    questions = []

    prompt = f"Erstelle ein Quiz über {category} mit jeweils {num_options} Antwortoptionen. Gib für jede Frage an, welche Option die korrekte Antwort ist."
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful quiz generator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3
    )

    generated_content = response.choices[0].message.content
    lines = generated_content.split("\n")

    question_text = ""
    options = []
    correct_option_index = None
    for line in lines:
        line = line.strip()
        if line.lower().startswith("frage"):
            if question_text and len(options) == num_options:  # Ensure the last question is added
                questions.append({
                    'question_text': question_text,
                    'options': options,
                    'correct_option_index': correct_option_index
                })
                if len(questions) == num_questions:  # Limit the number of questions
                    break
            # Reset for new question
            question_text = line.split(':', 1)[1].strip()
            options = []
            correct_option_index = None
        elif line and line[0].isalpha() and line[1] == ')':
            options.append(line[3:].strip())
        elif "richtige antwort" in line.lower():
            correct_option_index = len(options) - 1  # Index of the correct option

    # Add the last question if it wasn't already added
    if question_text and len(options) == num_options and len(questions) < num_questions:
        questions.append({
            'question_text': question_text,
            'options': options,
            'correct_option_index': correct_option_index
        })

    return questions[:num_questions]  # Return only the required number of questions


def save_quiz(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        quiz_id = request.POST.get('quiz_id')

        if category and quiz_id:
            try:
                quiz = Quiz.objects.get(id=quiz_id)
                for key, value in request.POST.items():
                    if key.startswith('user_answer'):
                        question_id = key.split('_')[-1]
                        option_id = int(value)

                        question = Question.objects.get(id=question_id)
                        selected_option = Option.objects.get(id=option_id)

                        UserAnswer.objects.create(
                            question=question,
                            selected_choice=selected_option
                        )

                return JsonResponse({'message': 'Quiz saved successfully!'})
            except Quiz.DoesNotExist:
                return JsonResponse({'error': 'Quiz not found.'}, status=404)
            except (Question.DoesNotExist, Option.DoesNotExist):
                return JsonResponse({'error': 'Question or Option not found.'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Missing category or quiz ID.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def saved_quizzes(request):
    # Fetch all saved quizzes
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/saved_quizzes.html', {'quizzes': quizzes})


def view_quiz(request, quiz_id):
    # Logik zum Anzeigen des Quiz
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/view_quiz.html', {'quiz': quiz})


def check_answers(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        results = []
        for question in quiz.questions.all():
            # Hier wird versucht, die ausgewählte Option zu erhalten
            selected_option_id = request.POST.get(f'user_answer_{question.id}')
            if selected_option_id:
                try:
                    selected_option = question.choices.get(id=selected_option_id)
                    is_correct = selected_option.is_correct
                    # Hier wird versucht, die korrekte Option zu erhalten
                    correct_option = question.choices.get(is_correct=True)
                    results.append({
                        'question_id': question.id,
                        'selected_option_id': selected_option_id,
                        'is_correct': is_correct,
                        'correct_option_text': correct_option.text if is_correct else None
                    })
                except Option.DoesNotExist:
                    # Wenn die Option nicht existiert, fügen Sie einen Fehler hinzu
                    results.append({
                        'question_id': question.id,
                        'error': 'Option does not exist.'
                    })
        return JsonResponse({'results': results})
    else:
        return JsonResponse({'error': 'This method is not allowed'}, status=405)
