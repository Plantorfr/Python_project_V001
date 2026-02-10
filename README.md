# 🔒 Analyseur Email Simplifié

Détection de phishing avec **BeautifulSoup** et **Regex**.

---

## 📦 Installation

```bash
# Installer BeautifulSoup4
pip install beautifulsoup4

# C'est tout ! 
```

---

## 🚀 Utilisation

```bash
python __main__.py email_test.eml
```

---

## 🏗️ Architecture Simple

```
__main__.py           → Point d'entrée CLI
email_parser.py       → BeautifulSoup + Regex pour parser
detection_rules.py    → Regex pour détecter anomalies
risk_scorer.py        → Calcul score simple
exporters.py          → Export rapport.txt
```

---

## 🔍 Librairies Utilisées

| Librairie | Utilisation | Justification |
|-----------|-------------|---------------|
| **BeautifulSoup4** | email_parser.py | Parse HTML dans emails (`.get_text()`) |
| **re (regex)** | Tous | Extraction patterns (URLs, domaines, mots-clés) |

**Pourquoi BeautifulSoup ?**
- Parse le HTML des emails automatiquement
- Extrait le texte proprement (retire les balises)
- API simple : `soup.get_text()`

**Pourquoi Regex ?**
- Extraction d'URLs : `https?://[^\s]+`
- Extraction de domaines : `@([\w\.-]+)`
- Détection mots-clés : `\b(urgent|cliquez)\b`
- Rapide et efficace

---

## 📊 Exemple de Regex

### Extraction d'URLs
```python
# Pattern : https?://[^\s<>"]+ 
# https? = http ou https
# [^\s<>"]+ = tout sauf espace, <, >, "

urls = re.findall(r'https?://[^\s<>"]+', texte)
```

### Extraction de domaine
```python
# Pattern : @([\w\.-]+)
# @ = arobase
# ([\w\.-]+) = capture lettres, chiffres, points, tirets

domaine = re.search(r'@([\w\.-]+)', email).group(1)
```

### Détection de mots-clés
```python
# Pattern : \b(urgent|cliquez)\b
# \b = frontière de mot
# (urgent|cliquez) = un OU l'autre

if re.search(r'\b(urgent|cliquez)\b', texte, re.IGNORECASE):
    print("Mot suspect trouvé !")
```

---

## 🎯 Règles de Détection

**1. Expéditeur suspect**
- Domaine avec >2 tirets ou >3 chiffres
- Reply-To ≠ From

**2. URLs suspectes**
- Raccourcisseurs (bit.ly, tinyurl)
- Adresse IP dans l'URL

**3. Mots-clés phishing**
- urgent, action requise, cliquez ici
- compte bloqué, confirmer, mot de passe

---

## 📈 Score

| Sévérité | Points |
|----------|--------|
| Faible | +10 |
| Moyenne | +25 |
| Haute | +40 |

**Niveaux** :
- 0-29 : Faible
- 30-59 : Moyen
- 60-100 : Critique

---

## ✅ Test

```bash
python __main__.py email_test.eml

# Résultat attendu :
# Score : 90/100 - CRITIQUE
# Anomalies : 5-6
```

---

## 📝 Code Ultra-Simplifié

**Parsing (BeautifulSoup)** :
```python
soup = BeautifulSoup(html, 'html.parser')
texte = soup.get_text()  # Retire les balises HTML
```

**Détection (Regex)** :
```python
urls = re.findall(r'https?://[^\s]+', texte)
mots = re.findall(r'\b(urgent|cliquez)\b', texte)
```

**Scoring** :
```python
score = sum(POINTS[a['severite']] for a in anomalies)
```

---

## 👥 Équipe

| Membre | Module |
|--------|--------|
| Moha | email_parser.py (BeautifulSoup) |
| Matt | detection_rules.py (Regex) |
| Micha | risk_scorer.py |
| Thibault | exporters.py |

---

C'est simple, clair et efficace ! 🚀
