from django.http import HttpResponse
from .models import Interaction

def enregistrer_interaction(request):
    if request.method == "POST":
        question = request.POST.get("question")
        reponse = request.POST.get("reponse")
        solution = request.POST.get("solution")

        if question and reponse and solution:
            Interaction.objects.create(
                question=question,
                reponse=reponse,
                solution=solution
            )
            return HttpResponse("Interaction enregistrée.")
        else:
            return HttpResponse("Données manquantes.", status=400)

