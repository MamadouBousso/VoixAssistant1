import pytest
import requests
from unittest.mock import MagicMock, patch
from src.infrastructure.openai_client import OpenAIClient

@pytest.fixture
def mock_requests_post():
    """Fixture pour mocker requests.post en utilisant unittest.mock."""
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "Ceci est une réponse de test."}}
            ]
        }
        mock_post.return_value = mock_response
        yield mock_post

def test_get_chat_completion_success(mock_requests_post):
    """Teste une complétion de chat réussie en utilisant un mock."""
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        client = OpenAIClient()
        prompt = "Salut, comment ça va ?"
        response = client.get_chat_completion(prompt)

        assert response == "Ceci est une réponse de test."
        mock_requests_post.assert_called_once()
        args, kwargs = mock_requests_post.call_args
        assert args[0] == OpenAIClient.API_URL
        assert kwargs["headers"]["Authorization"] == "Bearer test_key"
        assert kwargs["json"]["messages"][0]["content"] == prompt

def test_init_no_api_key():
    """Teste que l'initialisation échoue si la clé API n'est pas définie."""
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError, match="La clé API OpenAI n'est pas définie"):
            OpenAIClient()

def test_api_error(mock_requests_post):
    """Teste la gestion d'une erreur de l'API (ex: status code 500)."""
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        mock_requests_post.side_effect = requests.exceptions.HTTPError("Erreur serveur")
        
        client = OpenAIClient()
        response = client.get_chat_completion("un prompt")

        assert response is None 