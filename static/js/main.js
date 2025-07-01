/**
 * Gère l'interactivité de l'interface utilisateur du chat, y compris
 * la saisie vocale, la synthèse vocale et l'envoi de fichiers.
 */
document.addEventListener('DOMContentLoaded', () => {
    // --- Récupération des éléments du DOM ---
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const textInput = document.getElementById('text_input');
    const inputForm = document.getElementById('input-form');
    const loadingIndicator = document.getElementById('loading-indicator');
    const chatContainer = document.getElementById('chat-container');
    const speakResponseBtns = document.querySelectorAll('.speak-btn');
    const attachFileBtn = document.getElementById('attach-file-btn');
    const fileInput = document.getElementById('file-input');
    const fileDataInput = document.getElementById('file_data');
    const filePreviewContainer = document.getElementById('file-preview-container');
    const imagePreviewWrapper = document.getElementById('image-preview-wrapper');
    const imagePreview = document.getElementById('image-preview');
    const pdfPreviewWrapper = document.getElementById('pdf-preview-wrapper');
    const pdfName = document.getElementById('pdf-name');
    const removeFileBtn = document.getElementById('remove-file-btn');

    // Faire défiler le chat vers le bas au chargement de la page
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // --- Gestion de l'envoi de fichiers ---
    attachFileBtn.addEventListener('click', () => {
        fileInput.click(); // Ouvre le sélecteur de fichiers du navigateur
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            // Stocke le contenu du fichier (encodé en base64) dans un champ caché
            fileDataInput.value = e.target.result;
            filePreviewContainer.classList.remove('hidden');

            // Affiche l'aperçu approprié (image ou icône PDF)
            if (file.type.startsWith('image/')) {
                imagePreview.src = e.target.result;
                imagePreviewWrapper.classList.remove('hidden');
                pdfPreviewWrapper.classList.add('hidden');
            } else if (file.type === 'application/pdf') {
                pdfName.textContent = file.name;
                pdfPreviewWrapper.classList.remove('hidden');
                imagePreviewWrapper.classList.add('hidden');
            }
        };
        reader.readAsDataURL(file); // Lit le fichier comme une URL de données (base64)
    });

    removeFileBtn.addEventListener('click', () => {
        // Réinitialise tous les champs et aperçus liés au fichier
        fileInput.value = '';
        fileDataInput.value = '';
        filePreviewContainer.classList.add('hidden');
        imagePreviewWrapper.classList.add('hidden');
        pdfPreviewWrapper.classList.add('hidden');
        imagePreview.src = '#';
        pdfName.textContent = '';
    });


    // --- Gestion de la reconnaissance vocale (Web Speech API) ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = 'fr-FR'; // Définit la langue pour la reconnaissance
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        voiceInputBtn.addEventListener('click', () => {
            speechSynthesis.cancel(); // Arrête toute lecture en cours
            recognition.start();
        });

        recognition.addEventListener('start', () => {
            voiceInputBtn.classList.add('recording'); // Indication visuelle
        });

        // Lorsque la reconnaissance vocale produit un résultat final
        recognition.addEventListener('result', (e) => {
            const transcript = e.results[0][0].transcript;
            textInput.value = transcript; // Met le texte dans le champ de saisie
            inputForm.submit(); // Soumet le formulaire automatiquement
        });

        recognition.addEventListener('speechend', () => {
            recognition.stop();
            voiceInputBtn.classList.remove('recording');
        });

        recognition.addEventListener('error', (e) => {
            console.error(`Erreur de reconnaissance vocale : ${e.error}`);
            voiceInputBtn.classList.remove('recording');
        });
    } else {
        // Cache le bouton si l'API n'est pas supportée par le navigateur
        voiceInputBtn.style.display = 'none';
        console.warn('La reconnaissance vocale n\'est pas supportée par ce navigateur.');
    }

    // Affiche l'indicateur de chargement lors de la soumission du formulaire
    inputForm.addEventListener('submit', () => {
        loadingIndicator.classList.remove('hidden');
        // On pourrait masquer le chat ici pour éviter les doubles clics, mais ce n'est pas essentiel.
        // chatContainer.style.display = 'none';
    });


    // --- Gestion de la synthèse vocale (Web Speech API) ---
    if (speakResponseBtns) {
        speakResponseBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                speechSynthesis.cancel(); // Annule la lecture précédente
                
                const targetId = btn.getAttribute('data-target');
                const responseText = document.getElementById(targetId).innerText;
                const utterance = new SpeechSynthesisUtterance(responseText);
                utterance.lang = 'fr-FR'; // Définit la langue pour la synthèse
                speechSynthesis.speak(utterance); // Lit le texte
            });
        });
    }
}); 