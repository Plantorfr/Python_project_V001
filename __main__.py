"""
Point d'entrée du programme (VERSION SIMPLIFIÉE)

Utilisation : python __main__.py fichier.eml
"""

import sys
from email_parser import parser_email
from detection_rules import detecter_anomalies
from risk_scorer import evaluer_risque
from exporters import exporter_rapport


def afficher_banniere():
    """Affiche le titre"""
    print("\n" + "=" * 60)
    print("  🔒 ANALYSEUR EMAIL SIMPLIFIÉ")
    print("=" * 60 + "\n")


def analyser_email(fichier: str):
    """
    Analyse complète d'un email
    
    Pipeline simple :
    1. Parser l'email (BeautifulSoup + Regex)
    2. Détecter anomalies (Regex)
    3. Calculer score
    4. Exporter rapport
    """
    print(f"📂 Analyse de : {fichier}\n")
    
    # Étape 1 : Parsing
    print("[1/4] Parsing avec BeautifulSoup + Regex...")
    donnees = parser_email(fichier)
    print(f"      ✓ Expéditeur : {donnees['expediteur']}")
    
    # Étape 2 : Détection
    print("[2/4] Détection avec Regex...")
    anomalies = detecter_anomalies(donnees)
    print(f"      ✓ {len(anomalies)} anomalies trouvées")
    
    # Étape 3 : Scoring
    print("[3/4] Calcul du score...")
    evaluation = evaluer_risque(anomalies)
    print(f"      ✓ Score : {evaluation['score']}/100")
    
    # Étape 4 : Export
    print("[4/4] Export rapport...")
    rapport = exporter_rapport(donnees, anomalies, evaluation)
    print(f"      ✓ Rapport : {rapport}")
    
    # Résumé
    print("\n" + "=" * 60)
    print(f"🎯 RÉSULTAT : {evaluation['score']}/100 - {evaluation['niveau'].upper()}")
    print("=" * 60 + "\n")


def main():
    """Point d'entrée principal"""
    afficher_banniere()
    
    # Vérification argument
    if len(sys.argv) < 2:
        print("Usage : python __main__.py fichier.eml\n")
        return
    
    # Analyse
    try:
        analyser_email(sys.argv[1])
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {sys.argv[1]}")
    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
