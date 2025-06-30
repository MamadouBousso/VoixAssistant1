# Assistant IA Avancé

Ce projet est une application web d'assistant IA, conçue comme une base robuste et évolutive pour des interactions complexes. Elle intègre des fonctionnalités avancées telles que la reconnaissance vocale, l'analyse de fichiers (images et PDF), et une architecture logicielle professionnelle.

## Principes d'Architecture

Le projet est construit sur une **architecture hexagonale (Ports & Adapters)**. Ce choix de conception vise à isoler la logique métier des détails d'infrastructure, offrant une flexibilité, une testabilité et une maintenabilité maximales.

### 1. La Couche `Domaine` (`src/domaine`)
C'est le cœur de l'application. Elle contient la logique et les entités métier, pures et sans aucune dépendance à un framework ou une base de données.
-   `Message`: Représente un message unique (de l'utilisateur, de l'assistant ou du système).
-   `Conversation`: Agit comme une racine d'aggrégat (DDD), encapsulant une liste de `Message` et garantissant la cohérence de l'échange.

### 2. La Couche `Application` (`src/application`)
Elle orchestre les cas d'utilisation de l'application.
-   **Services (`chat_service.py`)**: Contient la logique applicative (ex: "traiter une requête utilisateur"). Il utilise les entités du domaine et interagit avec le monde extérieur via des ports.
-   **Ports (`ports/`)**: Ce sont des interfaces (contrats) qui définissent comment la couche application communique avec les services externes. Par exemple, `AIClient` définit ce que doit pouvoir faire un client d'IA, quel qu'il soit.

### 3. La Couche `Infrastructure` (`src/infrastructure`)
Elle fournit les implémentations concrètes des ports. C'est le "monde extérieur".
-   **Adapters**: Chaque classe ici est un "adapter" qui implémente un port et le connecte à un outil spécifique. `OpenAIClient` est un adapter qui connecte le port `AIClient` à l'API d'OpenAI. `PyMuPDFProcessor` fait de même pour la lecture de PDF.
-   **Factory (`ai_client_factory.py`)**: Utilise le patron de conception **Factory** pour créer et fournir le client IA demandé (OpenAI, Claude, etc.), en fonction de la configuration. Cela permet de changer de fournisseur d'IA sans modifier le code métier.

### 4. Le Point d'Entrée (`app.py`)
C'est la couche la plus externe, qui gère les interactions avec l'utilisateur (ici, via le web avec Flask).
-   Il est responsable de l'**injection de dépendances dynamique** : à chaque requête, il utilise la `AIClientFactory` pour instancier le client IA choisi par l'utilisateur dans l'interface.
-   Il gère les routes HTTP, les sessions utilisateur et la présentation des données via les templates HTML.

## Fonctionnalités Clés
-   **Conversation Contextuelle** : Maintien de l'historique des échanges.
-   **Analyse Multi-modale** : Traitement de requêtes contenant du texte, des images et des fichiers PDF.
-   **Choix Dynamique de Modèle** : L'utilisateur peut sélectionner son fournisseur d'IA (OpenAI, Claude, etc.) directement depuis l'interface.
-   **Interaction Vocale** : Saisie des questions et lecture des réponses.

## Installation et Lancement

#### Prérequis
-   Python 3.7+
-   Un navigateur web moderne (Chrome, Firefox, etc.) pour les fonctionnalités vocales.

#### Étapes

1.  **Cloner le dépôt**
    ```bash
    git clone [URL_DE_VOTRE_DEPOT]
    cd [NOM_DU_DOSSIER_DU_PROJET]
    ```

2.  **Créer un environnement virtuel** (recommandé)
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate  # Windows
    ```

3.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer l'environnement**
    -   Renommez `.env.example` en `.env`.
    -   Modifiez le fichier `.env` avec vos informations :
    ```env
    # --- Clés d'API pour les différents fournisseurs ---
    OPENAI_API_KEY="votre_cle_api_openai_ici"
    ANTHROPIC_API_KEY="votre_cle_api_anthropic_ici"
    GOOGLE_API_KEY="votre_cle_api_google_ici"

    # --- Configuration du fournisseur actif ---
    # Choisissez le fournisseur à utiliser. Options : "openai", "claude", "gemini"
    AI_PROVIDER="openai"
    ```

5.  **Lancer l'application**
    ```bash
    python app.py
    ```
    L'assistant est maintenant accessible à l'adresse `http://127.0.0.1:8081`.

## Structure du projet

```
.
├── app.py                  # Point d'entrée web (Flask)
├── requirements.txt        # Dépendances Python
├── src/
│   ├── application/
│   │   ├── ports/
│   │   └── chat_service.py
│   ├── domaine/
│   │   ├── message.py
│   │   └── conversation.py
│   └── infrastructure/
│       ├── ai_client_factory.py # Factory pour les clients IA
│       ├── claude_client.py     # Adapter (fictif) pour Claude
│       ├── gemini_client.py     # Adapter (fictif) pour Gemini
│       ├── openai_client.py     # Adapter pour OpenAI
│       └── pdf_processor.py     # Adapter pour le traitement PDF
├── static/
├── templates/
└── README.md
```
