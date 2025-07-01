from abc import ABC, abstractmethod
from typing import List, Dict

class AIClient(ABC):
    """
    Définit une interface (Port) pour un client d'intelligence artificielle.

    Dans l'architecture hexagonale, un Port est une interface qui définit un point
    d'interaction entre le cœur de l'application (le domaine et les services
    applicatifs) et le monde extérieur (l'infrastructure).

    Cette interface abstraite garantit que n'importe quel client d'IA
    (OpenAI, Claude, Gemini, etc.) peut être utilisé par l'application, tant
    qu'il respecte ce contrat. Cela découple la logique métier de
    l'implémentation spécifique d'une API externe.
    """

    @abstractmethod
    def get_chat_completion(self, messages: List[Dict], model: str) -> str:
        """
        Obtient une complétion de chat à partir d'un modèle d'IA.

        Cette méthode doit être implémentée par chaque "Adapter" concret.

        Args:
            messages (List[Dict]): Une liste de dictionnaires de messages,
                                   représentant l'historique de la conversation.
            model (str): Le nom du modèle à utiliser pour la complétion.

        Returns:
            Le contenu textuel du message de réponse de l'IA.
        """
        pass 