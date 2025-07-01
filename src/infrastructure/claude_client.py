import os
from typing import List, Dict

import anthropic
from dotenv import load_dotenv

from src.application.ports.ai_client import AIClient

load_dotenv()

class ClaudeClient(AIClient):
    """
    Adapter concret pour l'API d'Anthropic (Claude), implémentant AIClient.
    """
    def __init__(self):
        """Initialise le client Anthropic."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API Anthropic (Claude) n'est pas définie.")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def get_chat_completion(self, messages: List[Dict], model: str = "claude-3-opus-20240229") -> str:
        """
        Envoie une requête de complétion de chat à l'API Claude.
        
        Note : Claude attend un message système séparé et n'accepte pas le rôle 'system'
        dans la liste de messages principale. Cette méthode adapte le format.
        """
        system_prompt = ""
        # Sépare le message système du reste de la conversation
        if messages and messages[0]['role'] == 'system':
            system_prompt = messages[0]['content']
            messages_for_api = messages[1:]
        else:
            messages_for_api = messages

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages_for_api
            )
            return response.content[0].text
        except Exception as e:
            print(f"Une erreur API est survenue avec Claude : {e}")
            return "Désolé, une erreur est survenue lors de la communication avec Claude." 