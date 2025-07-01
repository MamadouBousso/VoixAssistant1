import requests

def get_dad_joke() -> str:
    """
    Récupère une blague (dad joke) depuis l'API icanhazdadjoke.com.
    Returns:
        str: La blague récupérée, ou un message d'erreur.
    """
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json", "User-Agent": "VoixAssistant/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("joke", "Pas de blague trouvée.")
    except Exception as e:
        return f"Erreur lors de la récupération de la blague : {e}" 