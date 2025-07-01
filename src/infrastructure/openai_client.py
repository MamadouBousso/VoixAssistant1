import os
import requests
from dotenv import load_dotenv
from typing import List, Dict

from src.application.ports.ai_client import AIClient

load_dotenv()

class OpenAIClient(AIClient):
    """
    Implémentation concrète (Adapter) du port AIClient pour l'API d'OpenAI.

    Cette classe adapte l'interface générique `AIClient` définie dans l'application
    aux spécificités de l'API OpenAI. Elle gère la construction de la requête HTTP,
    l'authentification et l'interprétation de la réponse.
    """
    API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self):
        """Initialise le client en chargeant la clé d'API depuis les variables d'environnement."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API OpenAI n'est pas définie. Veuillez la définir dans votre fichier .env")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_chat_completion(self, messages: List[Dict], model: str = "gpt-3.5-turbo") -> str:
        """
        Envoie une requête de complétion de chat à l'API OpenAI.

        Args:
            messages (List[Dict]): L'historique de la conversation.
            model (str): Le modèle OpenAI à utiliser (ex: 'gpt-3.5-turbo', 'gpt-4o').

        Returns:
            La réponse textuelle de l'assistant.
        """
        data = {
            "model": model,
            "messages": messages
        }
        try:
            response = requests.post(self.API_URL, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            print(f"Une erreur API est survenue : {e}")
            # Dans une application réelle, il faudrait un logger et une gestion d'erreurs plus fine.
            return "Désolé, une erreur est survenue lors de la communication avec l'IA." 