from dataclasses import dataclass, field
from typing import List, Dict
from .message import Message

@dataclass
class Conversation:
    """
    Représente une entité Conversation, qui est un aggrégat de Messages.

    Dans le DDD (Domain-Driven Design), cette classe est une racine d'aggrégat.
    Elle encapsule une liste de Messages et garantit la cohérence de l'ensemble
    de la conversation. Toutes les modifications de l'historique des messages
    doivent passer par cette classe.

    Attributes:
        messages (List[Message]): La liste des messages qui composent la conversation.
    """
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message):
        """
        Ajoute un message à la fin de l'historique de la conversation.

        C'est la seule méthode qui devrait être utilisée pour modifier l'état de la
        conversation, préservant ainsi l'invariant de l'aggrégat.

        Args:
            message (Message): L'objet Message à ajouter.
        """
        self.messages.append(message)

    def to_dict_list(self) -> List[Dict]:
        """
        Convertit l'ensemble de la conversation en une liste de dictionnaires.

        Utile pour la sérialisation de l'historique complet, par exemple pour
        le stocker dans une session ou l'envoyer à une API.

        Returns:
            Une liste de messages, où chaque message est un dictionnaire.
        """
        return [msg.to_dict() for msg in self.messages]

    @classmethod
    def from_dict_list(cls, data: List[Dict]):
        """
        Crée une instance de Conversation à partir d'une liste de dictionnaires.

        Cette méthode de fabrique (Factory Method) est utilisée pour la
        désérialisation, par exemple pour reconstruire une conversation
        à partir de données stockées dans une session.

        Args:
            data (List[Dict]): Une liste de dictionnaires, chacun représentant un message.

        Returns:
            Une nouvelle instance de la classe Conversation.
        """
        if not data:
            return cls()
        messages = [Message(**msg_data) for msg_data in data]
        return cls(messages=messages) 