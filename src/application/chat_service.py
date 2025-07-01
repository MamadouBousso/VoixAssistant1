import base64
from typing import Tuple, Union, List, Dict

from src.application.ports.ai_client import AIClient
from src.application.ports.file_processor import FileProcessor
from src.domaine.conversation import Conversation
from src.domaine.message import Message

class ChatService:
    """
    Service applicatif qui orchestre la logique métier du chat.

    Ce service est le cœur de la couche application. Il ne contient aucune
    logique liée à un framework web (comme Flask) ou à des détails
    d'infrastructure. Il utilise les ports (interfaces) pour interagir avec
    les systèmes externes, et les entités du domaine pour gérer l'état.

    Attributes:
        ai_client (AIClient): Une instance d'un client IA qui respecte l'interface AIClient.
        file_processor (FileProcessor): Une instance d'un processeur de fichiers.
    """

    def __init__(self, ai_client: AIClient, file_processor: FileProcessor):
        """Initialise le service avec ses dépendances (injectées)."""
        self.ai_client = ai_client
        self.file_processor = file_processor

    def process_user_request(self, conversation: Conversation, user_prompt: str, file_data: str = None) -> Tuple[Conversation, str]:
        """
        Traite la requête complète d'un utilisateur.

        Cette méthode orchestre la création du message utilisateur, l'appel au
        service d'IA, et la mise à jour de la conversation avec la réponse.

        Args:
            conversation (Conversation): L'état actuel de la conversation.
            user_prompt (str): Le message textuel de l'utilisateur.
            file_data (str, optional): Les données d'un fichier joint, encodées en base64.

        Returns:
            Un tuple contenant la conversation mise à jour et la réponse textuelle de l'assistant.
        """
        user_message_content = self._build_user_content(user_prompt, file_data)
        
        if not user_message_content:
            return conversation, "Veuillez fournir un message ou un fichier."
            
        model = "gpt-4o" if file_data else "gpt-3.5-turbo"
        
        conversation.add_message(Message(role="user", content=user_message_content))
        
        response_text = self.ai_client.get_chat_completion(
            messages=conversation.to_dict_list(),
            model=model
        )
        
        conversation.add_message(Message(role="assistant", content=response_text))
        return conversation, response_text

    def _build_user_content(self, user_prompt: str, file_data: str) -> Union[str, List[Dict]]:
        """
        Construit le contenu du message utilisateur à partir du prompt et du fichier.

        Cette méthode privée gère la complexité de la création de messages
        multi-parties (texte + image) ou de l'injection de texte extrait de PDF.

        Args:
            user_prompt (str): Le texte de l'utilisateur.
            file_data (str): Les données du fichier en base64.

        Returns:
            Le contenu formaté pour l'API OpenAI (soit un str, soit une liste de dictionnaires).
        """
        content = []
        if not user_prompt and not file_data:
            return ""

        if file_data:
            header, encoded = file_data.split(",", 1)
            
            if "image" in header:
                if user_prompt:
                    content.append({"type": "text", "text": user_prompt})
                content.append({"type": "image_url", "image_url": {"url": file_data}})
            
            elif "pdf" in header:
                file_bytes = base64.b64decode(encoded)
                pdf_text = self.file_processor.extract_text_from_pdf(file_bytes)
                full_prompt = (
                    f"Analyse le contenu du PDF suivant et réponds à la question de l'utilisateur.\n\n"
                    f"--- CONTENU DU PDF ---\n{pdf_text}\n--- FIN DU PDF ---\n\n"
                    f"Question : {user_prompt or 'Fais un résumé du document.'}"
                )
                content.append({"type": "text", "text": full_prompt})
        
        elif user_prompt:
            content.append({"type": "text", "text": user_prompt})

        # Pour l'API OpenAI, si le contenu est une liste avec un seul élément texte,
        # il est préférable de passer juste la chaîne de caractères.
        if len(content) == 1 and content[0]["type"] == "text":
            return content[0]["text"]
            
        return content 