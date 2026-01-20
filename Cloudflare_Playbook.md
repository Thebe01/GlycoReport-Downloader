# Playbook opérateur — Vérification Cloudflare

## Objectif

Permettre une intervention **manuelle** et **sûre** pendant les challenges
Cloudflare, sans contournement, tout en minimisant l’activité automatisée.

---

## 1) Quand intervenir

Intervenez dès le log :

- **"Vérification Cloudflare détectée"**

Le navigateur est alors en pause et attend une action humaine.

---

## 2) Étapes d’intervention manuelle

1. **Passer au navigateur Chrome** ouvert par Selenium.
2. **Compléter le challenge Cloudflare** (checkbox, captcha, etc.).
3. Attendre que la page se stabilise (login visible ou page suivante).
4. **Revenir au terminal** et appuyer sur **Entrée** pour reprendre.

---

## 3) Informations à collecter (si échec)

- **Capture d’écran** la plus récente dans le dossier de logs.
- **URL courante** (log “En attente Cloudflare… url=…”).
- **Titre de page** si loggé.
- **Heure exacte** de l’échec (timestamp log).
- **Niveau debug** activé ou non.

---

## 4) Reprise en sécurité

- Une fois le challenge terminé, **ne pas cliquer frénétiquement**.
- Laisser la page se stabiliser avant de reprendre.
- Appuyer sur **Entrée** dans le terminal pour relancer l’automatisation.

---

## 5) Escalade (si boucle persistante)

- Vérifier que le **profil Chrome** est bien celui attendu.
- Vérifier que **Chrome n’est pas en mode headless**.
- Relancer avec `--debug` et conserver les captures.
- Réduire l’activité automatique en augmentant `quiet_seconds` et
  `deep_scan_interval`.

---

## 6) Notes

Ce playbook vise uniquement à **laisser l’utilisateur agir**. Il ne fournit
**aucune instruction de contournement**.
