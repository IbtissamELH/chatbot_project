from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Interaction
from backend.chatbot_engine_bert import SmartChatbot
from langdetect import detect
from googletrans import Translator
import openpyxl

# 🔁 Initialiser le chatbot
chatbot = SmartChatbot("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

# ✅ Vue de l’accueil
def home(request):
    return render(request, 'chatbot/home.html')

# ✅ Vue messenger (avec login requis)
@login_required(login_url='login')
def messenger_view(request):
    return render(request, 'chatbot/chat_messenger.html')

# ✅ Vue API appelée en AJAX avec traduction auto
@login_required(login_url='login')
def chatbot_api(request):
    if request.method == "POST":
        question = request.POST.get("question", "")
        if not question:
            return JsonResponse({'error': 'Question vide'}, status=400)

        langue = detect(question)
        response = chatbot.get_response(question)

        # Traduction automatique si langue ≠ français
        translator = Translator()
        response["réponse"] = translator.translate(response["réponse"], dest=langue).text
        response["solution"] = translator.translate(response["solution"], dest=langue).text

        return JsonResponse({
            'question': question,
            'reponse': response["réponse"],
            'solution': response["solution"],
            'langue': langue
        })
def home_view(request):
    return render(request, 'chatbot/home.html')

# ✅ Vue traditionnelle avec affichage dans page chat.html
def chatbot_view(request):
    response = None
    langue = "fr"

    if request.method == "POST":
        question = request.POST.get("question")
        if question:
            langue = detect(question)
            response = chatbot.get_response(question)

            # Traduction
            translator = Translator()
            reponse_trad = translator.translate(response['réponse'], dest=langue).text
            solution_trad = translator.translate(response['solution'], dest=langue).text

            # Enregistrement
            Interaction.objects.create(
                question=question,
                reponse=reponse_trad,
                solution=solution_trad
            )

            # Mise à jour réponse affichée
            response['réponse'] = reponse_trad
            response['solution'] = solution_trad

    return render(request, "chatbot/chat.html", {
        "result": response,
        "langue": langue
    })

# ✅ Vue historique
@login_required(login_url='login')
def historique_view(request):
    interactions = Interaction.objects.order_by('-date')
    return render(request, "chatbot/historique.html", {"interactions": interactions})

# ✅ Exporter vers Excel
@login_required(login_url='login')
def export_excel_view(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Interactions"
    ws.append(["Date", "Question", "Réponse", "Solution"])

    for i in Interaction.objects.order_by('-date'):
        ws.append([
            i.date.strftime('%Y-%m-%d %H:%M'),
            i.question, i.reponse, i.solution
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="interactions_chatbot.xlsx"'
    wb.save(response)
    return response

# ✅ Autres pages
def contact_view(request):
    return render(request, 'chatbot/Contact.html')

def about_view(request):
    return render(request, 'chatbot/About.html')

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'chatbot/Profil.html')
