import os
import openai
from django.shortcuts import render

# Stellen Sie sicher, dass der API-Key korrekt aus den Umgebungsvariablen geladen wird
# openai.api_key = os.getenv('OPENAI_API_KEY')


openai.api_key = "YOUR_API_KEY"


def ki_helfer_view(request):
    context = {}
    if request.method == 'POST':
        user_input = request.POST.get('question')

        # Überprüfen Sie, ob die Benutzereingabe vorhanden ist
        if not user_input:
            context['error'] = 'Bitte geben Sie eine Frage ein.'
        else:
            # Senden Sie die Anfrage an die OpenAI-API
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # oder ein anderes Modell Ihrer Wahl
                    prompt=user_input,
                    max_tokens=150
                )
                context['response'] = response.choices[0].text
            except Exception as e:
                context['error'] = f"Es gab einen Fehler bei der Anfrage: {str(e)}"

    return render(request, 'helfer/studies_helfer.html', context)
