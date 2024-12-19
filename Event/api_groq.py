import requests

# Fonction pour améliorer la description du sponsor
def ameliorer_description(description_utilisateur: str) -> str:
    """
    Envoie la description d'un sponsor à l'API Groq pour l'améliorer.

    :param description_utilisateur: La description fournie par l'utilisateur
    :return: La description améliorée par l'API Groq
    """
    # URL de l'API Flask
    url = 'http://127.0.0.1:5000/chat'

    # Création du prompt en intégrant la description de l'utilisateur
    prompt = f"Dans le cadre d'une application, peux-tu améliorer cette description d evenement pour une activite qui doit être brève et concise ? Donne-moi juste la description finale en anglais sous forme de paragraphe, sans introduction ni explication : {description_utilisateur}"

    # Structure de la requête POST avec le prompt
    data = {
        'prompt': prompt
    }

    # Envoi de la requête POST à l'API
    response = requests.post(url, json=data)

    # Vérification du statut de la réponse
    if response.status_code == 200:
        # Si la réponse est réussie, obtenir le texte de la réponse
        response_data = response.json()
        response_text = response_data.get('response', '')

        # Test si la réponse contient un ":" ou des guillemets
        if ':' in response_text:
            response_text=response_text.split(':', 1)[-1].strip()
            # Retourner la partie après le ":" (enlever les espaces)
            if '"' in response_text:
                # Retourner le texte entre les guillemets
                start = response_text.find('"') + 1
                end = response_text.find('"', start)
                response_text= response_text[start:end]
            return response_text
        elif '"' in response_text:
            # Retourner le texte entre les guillemets
            start = response_text.find('"') + 1
            end = response_text.find('"', start)
            return response_text[start:end]
        else:
            # Si aucune des conditions n'est remplie, retourner la réponse telle quelle
            return response_text
    else:
        # Si la réponse échoue, retourner un message d'erreur
        return f"Erreur {response.status_code}: {response.text}"

