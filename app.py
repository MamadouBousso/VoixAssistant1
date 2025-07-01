import os
from flask import Flask, render_template, request, session

# --- Importation des composants de l'architecture ---
# Cette section montre clairement les dépendances de la couche web envers la couche application.
from src.application.chat_service import ChatService
from src.infrastructure.ai_client_factory import AIClientFactory
from src.infrastructure.pdf_processor import PyMuPDFProcessor
from src.domaine.conversation import Conversation
from src.domaine.message import Message

# --- Configuration ---
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé secrète pour sécuriser les sessions Flask

# Instanciation des composants qui n'ont pas d'état de requête (stateless)
pdf_processor = PyMuPDFProcessor()
available_providers = list(AIClientFactory._clients.keys())

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Contrôleur web principal qui gère l'affichage et le traitement du chat.
    """
    # Initialisation des variables pour la requête
    error_message = None
    user_prompt_for_template = ''
    
    # Récupérer la conversation et le fournisseur sélectionné depuis la session
    conv_data = session.get('conversation', [])
    conversation = Conversation.from_dict_list(conv_data)
    selected_provider = session.get('ai_provider', 'openai')
    
    # Initialiser la conversation avec un message système si elle est nouvelle
    if not conversation.messages:
        system_prompt = "Tu es un assistant très utile. Tu es très professionnel et tu réponds avec des phrases courtes et précises."
        conversation.add_message(Message(role="system", content=system_prompt))

    if request.method == 'POST':
        user_prompt = request.form.get('text_input', '')
        user_prompt_for_template = user_prompt  # Garder une copie pour l'affichage
        file_data = request.form.get('file_data')
        selected_provider = request.form.get('ai_provider', 'openai')
        session['ai_provider'] = selected_provider

        try:
            ai_client = AIClientFactory.create_client(selected_provider)
            chat_service = ChatService(ai_client=ai_client, file_processor=pdf_processor)

            conversation, _ = chat_service.process_user_request(
                conversation=conversation,
                user_prompt=user_prompt,
                file_data=file_data
            )
            session['conversation'] = conversation.to_dict_list()
        except ValueError as e:
            # Si la factory échoue (ex: clé API manquante), on crée un message d'erreur
            error_message = f"Erreur de configuration pour '{selected_provider.capitalize()}'. Veuillez vérifier que la clé API est bien définie dans votre fichier .env. Détail : {e}"
            print(f"ERREUR DE CONFIGURATION : {e}")

        session.modified = True

    # Préparer l'historique pour le template
    chat_history = [
        msg.to_dict() for msg in conversation.messages if msg.role in ['user', 'assistant']
    ]
    
    for message in chat_history:
        if isinstance(message['content'], list):
            text_content = next((item.get('text', '') for item in message['content'] if item.get('type') == 'text'), '')
            message['content'] = text_content if text_content else "[Analyse d'un fichier en cours...]"

    return render_template(
        'index.html', 
        chat_history=chat_history,
        providers=available_providers,
        selected_provider=selected_provider,
        error_message=error_message,
        user_prompt=user_prompt_for_template
    )

if __name__ == '__main__':
    app.run(debug=True, port=8081)
