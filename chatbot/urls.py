from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('chat/', views.chatbot_view, name='chatbot_view'), 
    path('historique/', views.historique_view, name='historique_view'),
    path('export-excel/', views.export_excel_view, name='export_excel'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('chatbot/messenger/', views.messenger_view, name='messenger_view'),


    

 # Le chatbot
]
