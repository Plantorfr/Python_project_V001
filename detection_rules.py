"""
Module de détection des anomalies (VERSION SIMPLIFIÉE)

Responsable : Matt
Utilise : Regex uniquement
"""

import re


class MoteurDetection:
    """
    Détecte les comportements suspects avec des regex simples
    Approche minimaliste et efficace
    """
    
    def __init__(self):
        """Initialise le moteur"""
        self.anomalies = []
    
    def analyser_email(self, donnees_email: dict) -> list:
        """
        Analyse complète avec regex
        
        Returns:
            Liste des anomalies détectées
        """
        self.anomalies = []
        
        # Exécution des règles
        self._verifier_expediteur(donnees_email)
        self._detecter_urls_suspectes(donnees_email)
        self._detecter_mots_cles_phishing(donnees_email)
        
        return self.anomalies
    
    def _ajouter_anomalie(self, severite: str, description: str):
        """Ajoute une anomalie à la liste"""
        self.anomalies.append({
            'severite': severite,
            'description': description
        })
    
    def _verifier_expediteur(self, donnees: dict):
        """
        Vérifie l'expéditeur avec regex
        
        Regex : <(.+@.+)> = capture l'email entre <>
        """
        expediteur = donnees.get('expediteur', '')
        reply_to = donnees.get('reply_to', '')
        
        # Extraction du domaine avec regex
        # Pattern : @([\w\.-]+) = capture le domaine après @
        match_domaine = re.search(r'@([\w\.-]+)', expediteur)
        
        if match_domaine:
            domaine = match_domaine.group(1).lower()
            
            # Vérification de domaines suspects (beaucoup de chiffres/tirets)
            if domaine.count('-') > 2 or sum(c.isdigit() for c in domaine) > 3:
                self._ajouter_anomalie(
                    'moyenne',
                    f"Domaine suspect : {domaine}"
                )
        
        # Vérification Reply-To différent de From
        if reply_to and reply_to != expediteur:
            self._ajouter_anomalie(
                'haute',
                f"Reply-To différent : {reply_to}"
            )
    
    def _detecter_urls_suspectes(self, donnees: dict):
        """
        Détecte les URLs suspectes avec regex
        
        Regex : https?://[^\s]+ = capture toutes les URLs
        """
        corps = donnees.get('corps', '')
        
        # Extraction de toutes les URLs
        # Pattern : https?:// suivi de caractères non-espaces
        urls = re.findall(r'https?://[^\s<>"]+', corps, re.IGNORECASE)
        
        for url in urls:
            # URL raccourcie
            if re.search(r'(bit\.ly|tinyurl|t\.co|goo\.gl)', url, re.IGNORECASE):
                self._ajouter_anomalie(
                    'moyenne',
                    f"URL raccourcie : {url}"
                )
            
            # URL avec adresse IP
            # Pattern : \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} = détecte les IP
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                self._ajouter_anomalie(
                    'haute',
                    f"URL avec IP : {url}"
                )
    
    def _detecter_mots_cles_phishing(self, donnees: dict):
        """
        Recherche des mots-clés typiques du phishing
        
        Regex : \\b(urgent|cliquez ici|compte bloqué)\\b
        \\b = frontière de mot (word boundary)
        """
        sujet = donnees.get('sujet', '').lower()
        corps = donnees.get('corps', '').lower()
        texte = f"{sujet} {corps}"
        
        # Liste de mots-clés suspects
        mots_suspects = [
            'urgent', 'action requise', 'compte bloqué', 'cliquez ici',
            'vérifiez', 'confirmer', 'mot de passe', 'gagnant'
        ]
        
        mots_trouves = []
        
        # Recherche de chaque mot-clé avec regex
        for mot in mots_suspects:
            # Pattern : \b{mot}\b = mot exact (pas dans un autre mot)
            if re.search(rf'\b{re.escape(mot)}\b', texte, re.IGNORECASE):
                mots_trouves.append(mot)
        
        # Si plusieurs mots suspects
        if len(mots_trouves) >= 2:
            self._ajouter_anomalie(
                'haute',
                f"Mots-clés phishing : {', '.join(mots_trouves)}"
            )


# Fonction simple
def detecter_anomalies(donnees_email: dict) -> list:
    """
    Détecte les anomalies en une ligne
    
    Example:
        anomalies = detecter_anomalies(donnees)
    """
    moteur = MoteurDetection()
    return moteur.analyser_email(donnees_email)
