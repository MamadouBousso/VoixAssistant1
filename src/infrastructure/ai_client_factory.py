from src.application.ports.ai_client import AIClient
from src.infrastructure.openai_client import OpenAIClient
from src.infrastructure.claude_client import ClaudeClient
from src.infrastructure.gemini_client import GeminiClient

class AIClientFactory:
    """
    Implémente le patron de conception Factory (fabrique) pour créer des clients IA.

    Le but de cette factory est de centraliser la logique de création des différents
    clients IA (OpenAI, Claude, etc.). Elle découple le code de l'application
    (le point d'entrée `app.py`) de la connaissance des classes de clients concrètes.

    L'application demande simplement un client pour un "fournisseur" donné, et la
    factory se charge de retourner la bonne instance.
    """
    _clients = {
        "openai": OpenAIClient,
        "claude": ClaudeClient,
        "gemini": GeminiClient,
    }

    @classmethod
    def create_client(cls, provider_name: str) -> AIClient:
        """
        Crée et retourne une instance de client IA basée sur le nom du fournisseur.

        Cette méthode de classe agit comme le constructeur public pour la factory.

        Args:
            provider_name (str): Le nom du fournisseur ('openai', 'claude', 'gemini').
                                 La casse est ignorée.

        Returns:
            Une instance d'une classe qui implémente l'interface `AIClient`.

        Raises:
            ValueError: Si le `provider_name` n'est pas supporté.
        """
        provider_name = provider_name.lower()
        client_class = cls._clients.get(provider_name)

        if not client_class:
            raise ValueError(f"Fournisseur d'IA non supporté : {provider_name}. "
                             f"Les fournisseurs valides sont : {list(cls._clients.keys())}")
        
        return client_class() 