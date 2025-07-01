import fitz  # PyMuPDF
from src.application.ports.file_processor import FileProcessor

class PyMuPDFProcessor(FileProcessor):
    """
    Implémentation concrète (Adapter) du port FileProcessor pour les fichiers PDF.

    Cette classe utilise la bibliothèque PyMuPDF (via le module `fitz`) pour
    implémenter la logique d'extraction de texte définie par le port `FileProcessor`.
    """
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Extrait le texte d'un PDF à partir de son contenu binaire.

        Args:
            pdf_bytes (bytes): Le contenu binaire du fichier PDF.

        Returns:
            Le texte extrait, ou un message d'erreur si l'extraction échoue.
        """
        text = ""
        try:
            # `fitz.open` peut lire un document à partir d'un flux de bytes.
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            # Gestion d'erreur basique. Dans une application de production,
            # un logger serait plus approprié.
            print(f"Erreur lors de l'extraction du texte du PDF : {e}")
            return "Impossible d'extraire le contenu de ce PDF." 