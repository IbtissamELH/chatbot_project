from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('chat/', views.chatbot_view, name='chatbot_view'), 
    path('historique/', views.historique_view, name='historique_view'),
    path('export-excel/', views.export_excel_view, name='export_excel'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('chatbot/chat_messenger/', views.messenger_view, name='chat_messenger'),
    path('Profil/', views.profile_view, name='Profil'),
    path('Contact/', views.contact_view, name='Contact'),
    path('About/', views.about_view, name='About'),


    

 # Le chatbot
]

