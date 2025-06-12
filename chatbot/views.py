from django.shortcuts import render
from backend.chatbot_engine_bert import SmartChatbot
 # ou chatbot_engine selon ta version
from django.shortcuts import render
from .models import Interaction  # ⚠️ Assure-toi d’avoir ce modèle
from googletrans import Translator
from langdetect import detect

chatbot = SmartChatbot("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

def chatbot_view(request):
    response = None
    langue = "fr"
    translated_response = None

    if request.method == "POST":
        question = request.POST.get("question")
        if question:
            langue = detect(question)
            response = chatbot.get_response(question)

            # Traduire la réponse dans la langue détectée
            translator = Translator()
            reponse_traduite = translator.translate(response['réponse'], dest=langue).text
            solution_traduite = translator.translate(response['solution'], dest=langue).text

            # Remplacer la réponse originale
            response['réponse'] = reponse_traduite
            response['solution'] = solution_traduite

            # Enregistrer l’interaction originale (non traduite)
            Interaction.objects.create(
                question=question,
                reponse=reponse_traduite,
                solution=solution_traduite
            )
    return render(request, "chatbot/chat.html", {
        "result": response,
        "langue": langue
    })

from django.shortcuts import render

def home(request):
    return render(request, "chatbot/home.html")




def historique_view(request):
    interactions = Interaction.objects.order_by('-date')  # Derniers d’abord
    return render(request, "chatbot/historique.html", {"interactions": interactions})


import openpyxl
from django.http import HttpResponse

def export_excel_view(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Interactions"

    # En-têtes
    ws.append(["Date", "Question", "Réponse", "Solution"])

    # Données
    for interaction in Interaction.objects.order_by('-date'):
        ws.append([
            interaction.date.strftime('%Y-%m-%d %H:%M'),
            interaction.question,
            interaction.reponse,
            interaction.solution
        ])

    # Réponse HTTP avec fichier Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="interactions_chatbot.xlsx"'
    wb.save(response)
    return response



from django.http import JsonResponse
from langdetect import detect
from googletrans import Translator

# ✅ S’assurer que ton moteur est bien initialisé
chatbot = SmartChatbot("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

def chatbot_api(request):
    if request.method == "POST":
        question = request.POST.get("question", "")
        if not question:
            return JsonResponse({'error': 'Question vide'}, status=400)

        langue = detect(question)
        response = chatbot.get_response(question)

        # Traduction automatique
        translator = Translator()
        reponse_trad = translator.translate(response['réponse'], dest=langue).text
        solution_trad = translator.translate(response['solution'], dest=langue).text

        return JsonResponse({
            'question': question,
            'reponse': reponse_trad,
            'solution': solution_trad,
            'langue': langue
        })

def messenger_view(request):
    return render(request, "chatbot/chat_messenger.html")
