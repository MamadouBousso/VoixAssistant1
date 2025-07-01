from abc import ABC, abstractmethod

class FileProcessor(ABC):
    """
    Définit une interface (Port) pour un processeur de fichiers.

    Ce port abstrait la logique d'extraction de contenu à partir de différents
    types de fichiers (comme les PDF). Le but est de découpler le service
    applicatif de la bibliothèque ou de la méthode spécifique utilisée pour
    lire les fichiers.

    Si demain on souhaite changer de bibliothèque pour lire les PDF, ou ajouter
    le support pour les fichiers .docx, il suffira de créer un nouvel "Adapter"
    qui implémente cette interface, sans modifier le reste de l'application.
    """

    @abstractmethod
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Extrait le contenu textuel d'un fichier PDF fourni en bytes.

        Args:
            pdf_bytes (bytes): Le contenu binaire du fichier PDF.

        Returns:
            Le texte extrait du document.
        """
        pass 