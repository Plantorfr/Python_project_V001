"""
Module de parsing des emails au format .eml (VERSION SIMPLIFIÉE)

Responsable : Moha
Utilise : BeautifulSoup + Regex
"""

import re
from bs4 import BeautifulSoup


class AnalyseurEmail:
    """
    Parse un fichier .eml avec BeautifulSoup et regex
    Version minimaliste et claire
    """
    
    def __init__(self, chemin_fichier: str):
        """Initialise avec le chemin du fichier .eml"""
        self.chemin_fichier = chemin_fichier
        self.contenu_brut = ""
        self.entetes = {}
        self.corps = ""
    
    def charger_email(self):
        """
        Lit le fichier .eml
        Justification : Lecture simple en mode texte
        """
        with open(self.chemin_fichier, 'r', encoding='utf-8') as fichier:
            self.contenu_brut = fichier.read()
    
    def extraire_entetes(self):
        """
        Extrait les en-têtes avec regex
        
        Regex : ^(From|To|Subject|Date|Reply-To):(.+)$
        ^ = début de ligne
        (.+) = capture tout après les deux-points
        """
        # Pattern pour capturer les en-têtes principaux
        pattern = r'^(From|To|Subject|Date|Reply-To):\s*(.+)$'
        
        matches = re.findall(pattern, self.contenu_brut, re.MULTILINE | re.IGNORECASE)
        
        for nom, valeur in matches:
            self.entetes[nom.capitalize()] = valeur.strip()
    
    def extraire_corps(self):
        """
        Extrait le corps du message
        
        Logique : Le corps commence après la première ligne vide
        Regex : \n\n(.+) = tout après deux retours à la ligne
        """
        # Séparation en-têtes / corps à la première ligne vide
        parties = self.contenu_brut.split('\n\n', 1)
        
        if len(parties) > 1:
            self.corps = parties[1].strip()
        
        # Si le corps contient du HTML, on extrait le texte avec BeautifulSoup
        if '<html' in self.corps.lower() or '<body' in self.corps.lower():
            soup = BeautifulSoup(self.corps, 'html.parser')
            self.corps = soup.get_text(separator=' ', strip=True)
    
    def obtenir_donnees_completes(self) -> dict:
        """
        Retourne toutes les données extraites
        
        Returns:
            Dictionnaire simple et clair
        """
        self.charger_email()
        self.extraire_entetes()
        self.extraire_corps()
        
        return {
            'expediteur': self.entetes.get('From', 'Inconnu'),
            'destinataire': self.entetes.get('To', 'Inconnu'),
            'sujet': self.entetes.get('Subject', ''),
            'date': self.entetes.get('Date', ''),
            'reply_to': self.entetes.get('Reply-to', ''),
            'corps': self.corps
        }


# Fonction simple pour usage rapide
def parser_email(chemin_fichier: str) -> dict:
    """
    Parse un email en une ligne
    
    Example:
        donnees = parser_email('spam.eml')
    """
    analyseur = AnalyseurEmail(chemin_fichier)
    return analyseur.obtenir_donnees_completes()
