"""
Module de calcul du score de risque (VERSION SIMPLIFIÉE)

Responsable : Micha
Logique ultra-simple
"""


class CalculateurRisque:
    """
    Calcule un score simple basé sur la sévérité
    Formule claire et directe
    """
    
    # Points simples par sévérité
    POINTS = {
        'faible': 10,
        'moyenne': 25,
        'haute': 40
    }
    
    def calculer_score(self, anomalies: list) -> dict:
        """
        Calcule le score total
        
        Formule : Σ points par anomalie (max 100)
        """
        score = 0
        
        # Somme simple
        for anomalie in anomalies:
            severite = anomalie.get('severite', 'faible')
            score += self.POINTS.get(severite, 10)
        
        # Plafonnement à 100
        score = min(score, 100)
        
        # Détermination du niveau
        if score == 0:
            niveau = 'minimal'
        elif score < 30:
            niveau = 'faible'
        elif score < 60:
            niveau = 'moyen'
        else:
            niveau = 'critique'
        
        return {
            'score': score,
            'niveau': niveau,
            'nb_anomalies': len(anomalies)
        }


# Fonction simple
def evaluer_risque(anomalies: list) -> dict:
    """
    Évalue le risque en une ligne
    
    Example:
        resultat = evaluer_risque(anomalies)
    """
    calc = CalculateurRisque()
    return calc.calculer_score(anomalies)
