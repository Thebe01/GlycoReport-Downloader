# Audit Cloudflare — GlycoReport-Downloader (0.2.18)

**Objectif** : identifier les signaux détectables par Cloudflare dans ce dépôt,
proposer un plan d’amélioration sans contournement, et préciser un patch minimal
d’amélioration opérationnelle.

## 1) Signaux détectables par Cloudflare dans ce repo

### A. Signaux d’automatisation (empreinte WebDriver)

- **WebDriver actif** : Selenium expose des traces côté navigateur (ex.
  `navigator.webdriver`).
- **Chaîne d’options Chrome** : certains flags d’automatisation peuvent être
  corrélés par des contrôles Cloudflare (même si aucune interaction DOM n’est
  faite).
- **Pilotage programmatique** : WebDriver orchestre le navigateur et injecte un
  pattern d’exécution non-humain (timing très régulier, enchaînement d’actions
  rapides).

### B. Empreinte et cohérence du navigateur

- **Profil utilisateur** : usage d’un profil Chrome dédié (via
  `--user-data-dir`) peut diverger d’un profil “humain” habituel.
- **Flags de désactivation** : désactivation de fonctionnalités peut créer un
  environnement atypique (ex. `--disable-sync`, `--disable-translate`,
  `--disable-popup-blocking`).
- **Indicateurs matériels** : si le rendu GPU est réduit (ex. `--disable-gpu`),
  certains signaux graphiques sont moins “humains”.

### C. Comportements observables

- **Polling régulier** : boucle d’attente Cloudflare (même avec quiet window)
  effectue des contrôles périodiques.
- **Captures d’écran automatiques** : elles ne modifient pas la page, mais
  impliquent un pattern automation.
- **Transitions rapides** : séquences d’actions déterministes (ex. clic → sleep
  → saisie) peuvent être distinguées d’un comportement humain.

### D. Contexte d’exécution

- **Environnement automatisé** : exécution via Selenium/ChromeDriver, détectable
  par heuristiques côté serveur.

> **Important** : l’objectif ici est d’**assurer une gestion propre** et
> **minimiser l’activité automatisée**, pas de contourner la vérification.

---

## 2) Plan d’amélioration priorisé (sans contournement)

### Quick wins (immédiat)

1. **Réduire le polling lors des challenges persistants** (backoff exponentiel
   côté attente Cloudflare). ✅
2. **Pause explicite et manuelle** dès détection Cloudflare (entrée utilisateur
   pour reprise). ✅
3. **Logs enrichis** (état, backoff, URLs). ✅
4. **Timeouts ajustables** pour éviter les boucles trop longues.

### Medium term (1–3 itérations)

1. **Paramétrer `quiet_seconds`/`deep_scan_interval`/`poll_seconds` via
   config.yaml**.
2. **Stabiliser le profil Chrome** (profils testés, extensions inchangées).
3. **Documentation d’exploitation** avec checklist Cloudflare (voir playbook).

### Long term (stratégique)

1. **Évaluer l’accès via API officielle** si disponible.
2. **Séparer la phase d’authentification** (manuel) et la phase de
   téléchargement (automatisée).
3. **Packaging operator-first** : état “pause” clair et explicite.

---

## 3) Patch minimal (résumé)

Le patch minimal inclut :

- Backoff exponentiel borné lors des challenges persistants.
- Pause manuelle par défaut (Entrée) après détection Cloudflare.
- Un test unitaire pour le helper de backoff.

Fichiers modifiés :

- [utils.py](utils.py)
- [tests/test_utils.py](tests/test_utils.py)

---

## 4) Playbook opérateur (voir document dédié)

Le playbook détaillé est dans :

- [Cloudflare_Playbook.md](Cloudflare_Playbook.md)
