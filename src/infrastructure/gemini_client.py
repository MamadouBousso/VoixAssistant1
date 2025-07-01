import os
from typing import List, Dict
import base64

import google.generativeai as genai
from dotenv import load_dotenv

from src.application.ports.ai_client import AIClient

load_dotenv()

class GeminiClient(AIClient):
    """
    Adapter concret pour l'API Google Gemini, implémentant AIClient.
    """
    def __init__(self):
        """Initialise le client Gemini."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API Google (Gemini) n'est pas définie.")
        genai.configure(api_key=self.api_key)

    def get_chat_completion(self, messages: List[Dict], model: str = "gemini-1.5-flash") -> str:
        """
        Envoie une requête de complétion de chat à l'API Gemini.

        Cette méthode adapte notre format de message interne à celui attendu par Gemini,
        notamment en traitant les images et en ajustant les rôles.
        """
        model_instance = genai.GenerativeModel(model)
        
        # Le message système est géré différemment
        system_prompt = ""
        if messages and messages[0]['role'] == 'system':
            system_prompt = messages[0]['content']
            messages = messages[1:]
        
        # Adaptation des messages pour l'historique de chat de Gemini
        # Gemini utilise 'model' pour le rôle de l'assistant.
        history_for_api = self._format_messages_for_gemini(messages[:-1])
        chat_session = model_instance.start_chat(history=history_for_api)

        # Le dernier message est celui à envoyer
        last_user_message = self._format_messages_for_gemini(messages[-1:])

        try:
            # Envoi du dernier message
            response = chat_session.send_message(last_user_message)
            return response.text
        except Exception as e:
            print(f"Une erreur API est survenue avec Gemini : {e}")
            return "Désolé, une erreur est survenue lors de la communication avec Gemini."

    def _format_messages_for_gemini(self, messages: List[Dict]) -> List[Dict]:
        """Convertit une liste de messages de notre format à celui de Gemini."""
        formatted = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            
            # Gestion des messages complexes (texte + image)
            if isinstance(msg["content"], list):
                parts = []
                for item in msg["content"]:
                    if item["type"] == "text":
                        parts.append(item["text"])
                    elif item["type"] == "image_url":
                        # Extrait le type MIME et les données de l'URL base64
                        header, encoded = item["image_url"]["url"].split(",", 1)
                        mime_type = header.split(";")[0].split(":")[1]
                        image_data = base64.b64decode(encoded)
                        parts.append({'mime_type': mime_type, 'data': image_data})
                formatted.append({"role": role, "parts": parts})
            else:
                # Message texte simple
                formatted.append({"role": role, "parts": [msg["content"]]})
        
        if len(formatted) == 1:
            return formatted[0]['parts']
            
        return formatted 