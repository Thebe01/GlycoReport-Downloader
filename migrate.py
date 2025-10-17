#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: migrate.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-10-16
#'''Last Modified On : 2025-10-16
#'''CopyRights : Pierre Théberge
#'''Description : Script de migration pour GlycoReport-Downloader.
#'''              Permet de migrer les configurations utilisateur entre versions.
#'''              - Supprime les paramètres obsolètes du config.yaml
#'''              - Nettoie les fichiers et dossiers devenus inutiles
#'''              - Crée des backups avant toute modification
#'''              - Affiche des messages colorés et informatifs
#'''Version : 1.0.0
#'''Modifications :
#'''Version   Date         Billet   Description
#'''1.0.0     2025-10-16   ES-12    Version initiale - Migration vers 0.2.4 (ChromeDriverManager)
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import sys
import shutil
from datetime import datetime
import yaml

# Import colorama pour les messages colorés (compatible avec config.py)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    # Fallback si colorama n'est pas installé
    class Fore:
        GREEN = YELLOW = RED = CYAN = ""
    class Style:
        RESET_ALL = ""

def print_success(message):
    """Affiche un message de succès en vert."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_warning(message):
    """Affiche un message d'avertissement en jaune."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def print_error(message):
    """Affiche un message d'erreur en rouge."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_info(message):
    """Affiche un message d'information en cyan."""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def backup_file(filepath):
    """Crée un backup d'un fichier avec timestamp."""
    if not os.path.exists(filepath):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    
    try:
        shutil.copy2(filepath, backup_path)
        print_success(f"Backup créé : {backup_path}")
        return backup_path
    except Exception as e:
        print_error(f"Impossible de créer le backup : {e}")
        return None

def remove_chromedriver_path_from_config(config_path="config.yaml"):
    """Supprime le paramètre chromedriver_path du fichier config.yaml."""
    
    print_info(f"\n{'='*60}")
    print_info("ÉTAPE 1 : Nettoyage du fichier config.yaml")
    print_info(f"{'='*60}")
    
    if not os.path.exists(config_path):
        print_warning(f"Le fichier {config_path} n'existe pas. Rien à faire.")
        return False
    
    # Lire le fichier config.yaml
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print_error(f"Erreur lors de la lecture de {config_path} : {e}")
        return False
    
    # Vérifier si chromedriver_path existe
    if 'chromedriver_path' not in config:
        print_success(f"Le paramètre 'chromedriver_path' n'est pas présent dans {config_path}.")
        print_info("Aucune modification nécessaire.")
        return False
    
    # Créer un backup
    print_info(f"Le paramètre 'chromedriver_path' a été trouvé : {config['chromedriver_path']}")
    backup_path = backup_file(config_path)
    
    if backup_path is None:
        print_error("Impossible de continuer sans backup. Migration annulée.")
        return False
    
    # Supprimer chromedriver_path
    del config['chromedriver_path']
    
    # Écrire le nouveau fichier
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print_success(f"Le paramètre 'chromedriver_path' a été supprimé de {config_path}")
        return True
    except Exception as e:
        print_error(f"Erreur lors de l'écriture de {config_path} : {e}")
        print_warning(f"Vous pouvez restaurer le backup : {backup_path}")
        return False

def remove_chromedriver_directory(chromedriver_dir="chromedriver-win64"):
    """Demande confirmation et supprime le répertoire chromedriver-win64."""
    
    print_info(f"\n{'='*60}")
    print_info("ÉTAPE 2 : Suppression du répertoire chromedriver-win64")
    print_info(f"{'='*60}")
    
    if not os.path.exists(chromedriver_dir):
        print_success(f"Le répertoire {chromedriver_dir} n'existe pas. Rien à faire.")
        return False
    
    if not os.path.isdir(chromedriver_dir):
        print_warning(f"{chromedriver_dir} n'est pas un répertoire. Ignoré.")
        return False
    
    # Afficher des informations sur le répertoire
    try:
        total_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(chromedriver_dir)
            for filename in filenames
        )
        size_mb = total_size / (1024 * 1024)
        print_info(f"Répertoire trouvé : {os.path.abspath(chromedriver_dir)}")
        print_info(f"Taille : {size_mb:.2f} MB")
    except Exception as e:
        print_warning(f"Impossible de calculer la taille : {e}")
    
    # Demander confirmation
    print_warning("\n⚠️  ATTENTION ⚠️")
    print_warning("Le répertoire 'chromedriver-win64' n'est plus nécessaire depuis la version 0.2.3.")
    print_warning("ChromeDriverManager télécharge automatiquement la version appropriée de ChromeDriver.")
    print_warning("")
    print_warning("Si vous utilisez ce répertoire pour d'autres applications, répondez 'non'.")
    print_warning("")
    
    while True:
        response = input(f"{Fore.CYAN}Voulez-vous supprimer le répertoire chromedriver-win64 ? (oui/non) : {Style.RESET_ALL}").strip().lower()
        
        if response in ['oui', 'o', 'yes', 'y']:
            # Supprimer le répertoire
            try:
                shutil.rmtree(chromedriver_dir)
                print_success(f"Le répertoire {chromedriver_dir} a été supprimé.")
                print_info(f"Espace libéré : ~{size_mb:.2f} MB")
                return True
            except Exception as e:
                print_error(f"Erreur lors de la suppression du répertoire : {e}")
                return False
        
        elif response in ['non', 'n', 'no']:
            print_info("Le répertoire a été conservé.")
            print_info("Vous pouvez le supprimer manuellement plus tard si nécessaire.")
            return False
        
        else:
            print_warning("Réponse invalide. Veuillez répondre par 'oui' ou 'non'.")

def main():
    """Point d'entrée principal du script de migration."""
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  Migration vers GlycoReport-Downloader v0.2.4")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    print_info("Ce script va :")
    print_info("  1. Supprimer le paramètre obsolète 'chromedriver_path' de config.yaml")
    print_info("  2. Proposer de supprimer le répertoire 'chromedriver-win64'")
    print_info("\nDes backups seront créés avant toute modification.")
    
    input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    # Étape 1 : Nettoyer config.yaml
    config_modified = remove_chromedriver_path_from_config()
    
    # Étape 2 : Supprimer le répertoire chromedriver-win64
    directory_removed = remove_chromedriver_directory()
    
    # Résumé
    print_info(f"\n{'='*60}")
    print_info("RÉSUMÉ DE LA MIGRATION")
    print_info(f"{'='*60}")
    
    if config_modified:
        print_success("config.yaml : Paramètre 'chromedriver_path' supprimé")
    else:
        print_info("config.yaml : Aucune modification nécessaire")
    
    if directory_removed:
        print_success("chromedriver-win64 : Répertoire supprimé")
    else:
        print_info("chromedriver-win64 : Répertoire conservé")
    
    print_info(f"\n{'='*60}")
    print_success("Migration terminée !")
    print_info(f"{'='*60}\n")
    
    print_info("Prochaines étapes :")
    print_info("  - ChromeDriverManager téléchargera automatiquement ChromeDriver au premier lancement")
    print_info("  - Aucune configuration supplémentaire n'est nécessaire")
    print_info("  - Vous pouvez lancer GlycoReport-Downloader normalement")
    
    print(f"\n{Fore.GREEN}Merci d'utiliser GlycoReport-Downloader !{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nMigration interrompue par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nErreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
