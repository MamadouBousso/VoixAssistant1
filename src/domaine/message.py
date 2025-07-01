from dataclasses import dataclass, asdict
from typing import Union, Literal

@dataclass
class Message:
    """
    Représente une entité Message dans le domaine de l'application.

    Cette classe est un objet de valeur (Value Object) qui encapsule les données d'un
    message unique au sein d'une conversation. Elle est immuable par nature
    (bien que dataclass ne le garantisse pas sans `frozen=True`) et représente
    un élément de l'historique des échanges.

    Attributes:
        role (Literal): Le rôle de l'auteur du message. Il ne peut être que
                        'user', 'assistant', ou 'system', conformément aux
                        conventions des API de chat.
        content (Union[str, list]): Le contenu du message.
                                    - Un `str` pour les messages textuels simples.
                                    - Une `list` pour les messages multi-parties
                                      (ex: un message contenant du texte et une image).
    """
    role: Literal["user", "assistant", "system"]
    # Le contenu peut être une simple chaîne de caractères ou une liste de parties
    # pour les messages complexes (texte + image).
    content: Union[str, list]

    def to_dict(self) -> dict:
        """
        Sérialise l'objet Message en un dictionnaire.

        Cette méthode est utile pour la persistance (ex: dans une session Flask)
        ou pour la transmission à des API externes qui attendent un format JSON.

        Returns:
            Un dictionnaire représentant l'objet Message.
        """
        return asdict(self) 