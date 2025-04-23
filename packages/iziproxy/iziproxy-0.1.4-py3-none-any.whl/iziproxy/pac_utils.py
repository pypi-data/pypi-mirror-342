"""
Module pour l'analyse et l'utilisation des fichiers PAC (Proxy Auto-Configuration).
"""

import os
import platform
import logging
import tempfile
import time
from typing import Dict, Optional, Union, Tuple
from urllib.parse import urlparse
import socket

logger = logging.getLogger(__name__)

# Variable pour stocker en cache les résultats des analyses PAC
_pac_cache = {}
# Durée de validité du cache en secondes (5 minutes par défaut)
PAC_CACHE_TTL = 300


class PacNotAvailableError(Exception):
    """Exception levée quand le support PAC est requis mais non disponible."""
    pass


def _get_pac_proxy(url: str, pac_url: Optional[str] = None, test_auth: bool = True) -> Dict[str, str]:
    """
    Fonction interne pour obtenir la configuration de proxy à partir d'un PAC.
    Cette fonction est séparée pour faciliter les tests.
    
    Args:
        url: URL pour laquelle déterminer le proxy
        pac_url: URL du fichier PAC à utiliser, ou None pour détection automatique
        test_auth: Si True, teste si le proxy nécessite une authentification
        
    Returns:
        Dictionnaire de configuration de proxy (http/https)
    """
    proxy_config = {}
    proxy_host = None
    
    try:
        # Importer le module pypac s'il est disponible
        if is_pac_available():
            import pypac
            from pypac import PACSession
            from pypac.parser import PACFile
            
            # Utiliser pypac pour analyser le fichier PAC
            if pac_url:
                # Si une URL PAC est spécifiée explicitement
                try:
                    import requests
                    # Télécharger le contenu du fichier PAC
                    response = requests.get(pac_url, timeout=10)
                    response.raise_for_status()  # Vérifier si la requête a réussi
                    pac_content = response.text
                    
                    # Analyser le contenu du fichier PAC
                    parsed_pac = PACFile(pac_content)
                    proxy_str = parsed_pac.find_proxy_for_url(url, urlparse(url).netloc)
                except Exception as e:
                    logger.warning(f"Erreur lors du téléchargement ou de l'analyse du fichier PAC: {e}")
                    proxy_str = ""
            else:
                # Utiliser la détection automatique de PAC
                try:
                    session = PACSession()
                    proxy_str = session.get_proxy_for_url(url)
                except pypac.PyPACError as e:
                    logger.debug(f"Erreur lors de la détection automatique PAC: {e}")
                    proxy_str = ""
                    
            # Convertir la chaîne de proxy au format attendu par requests
            if proxy_str and proxy_str.lower() != "direct":
                # Format typique: "PROXY proxy.example.com:8080; DIRECT"
                parts = proxy_str.split(";")[0].strip().split(" ", 1)
                if len(parts) > 1 and parts[0].upper() in ("PROXY", "HTTP"):
                    proxy_host = parts[1].strip()
                    proxy_config = {
                        "http": f"http://{proxy_host}",
                        "https": f"http://{proxy_host}"
                    }
    except Exception as e:
        logger.warning(f"Erreur lors de l'analyse PAC: {e}")
    
    # Tester si le proxy nécessite une authentification
    if test_auth and proxy_host and proxy_config:
        requires_auth = _test_proxy_auth_required(url, proxy_host)
        if requires_auth:
            # Obtenir les identifiants
            username, password = _get_proxy_credentials()
            if username and password:
                # Mettre à jour la configuration avec les identifiants
                proxy_config = {
                    "http": f"http://{username}:{password}@{proxy_host}",
                    "https": f"http://{username}:{password}@{proxy_host}"
                }
                logger.debug(f"Configuration proxy PAC mise à jour avec authentification")
    
    return proxy_config


def get_proxy_for_url(url: str, pac_url: Optional[str] = None, test_auth: bool = True) -> Dict[str, str]:
    """
    Détermine le proxy à utiliser pour une URL donnée à partir d'un fichier PAC.
    
    Args:
        url: URL pour laquelle déterminer le proxy
        pac_url: URL du fichier PAC à utiliser, ou None pour détection automatique
        
    Returns:
        Dictionnaire de configuration de proxy (http/https)
        
    Raises:
        PacNotAvailableError: Si le support PAC est requis mais non disponible
    """
    # Essayer d'utiliser le système de cache pour éviter des requêtes répétées
    cache_key = f"{url}:{pac_url}"
    current_time = time.time()
    
    # Vérifier si une entrée valide existe dans le cache
    if cache_key in _pac_cache:
        entry_time, cached_proxy_config = _pac_cache[cache_key]
        if current_time - entry_time < PAC_CACHE_TTL:
            logger.debug(f"Utilisation du cache PAC pour {url}")
            return cached_proxy_config.copy()  # Renvoyer une copie pour éviter les modifications
    
    # Obtenir la configuration de proxy via la fonction interne
    proxy_config = _get_pac_proxy(url, pac_url, test_auth)
    
    # Stocker le résultat dans le cache
    _pac_cache[cache_key] = (current_time, proxy_config)
    
    return proxy_config


def detect_system_pac_url() -> Optional[str]:
    """
    Détecte l'URL du fichier PAC configuré au niveau système.
    
    Returns:
        URL du fichier PAC ou None si non trouvé
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            # Tenter de lire la configuration Windows
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            ) as key:
                # Vérifier si la configuration automatique est activée
                try:
                    auto_config = winreg.QueryValueEx(key, "AutoConfigURL")[0]
                    if auto_config:
                        return auto_config
                except (FileNotFoundError, OSError):
                    pass
                    
        elif system == "Darwin":  # macOS
            # Méthode simplifiée pour macOS, pourrait nécessiter networksetup en réalité
            # En pratique, on pourrait exécuter `networksetup -getautoproxyurl Wi-Fi`
            return None
            
        elif system == "Linux":
            # Essayer de lire la configuration GNOME
            try:
                import subprocess
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.system.proxy", "autoconfig-url"],
                    capture_output=True, text=True, check=True
                )
                pac_url = result.stdout.strip().strip("'")
                if pac_url and pac_url != "''":
                    return pac_url
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
    except Exception as e:
        logger.debug(f"Erreur lors de la détection du PAC système: {e}")
        
    return None


def clear_pac_cache() -> None:
    """
    Efface le cache des résultats PAC.
    """
    global _pac_cache
    _pac_cache.clear()


def is_pac_available() -> bool:
    """
    Vérifie si le support PAC est disponible.
    
    Returns:
        True si le support PAC est disponible, False sinon
    """
    try:
        import pypac
        return True
    except ImportError:
        logger.warning("Le support PAC n'est pas disponible. Installez les dépendances avec 'pip install iziproxy[pac]' pour activer la détection automatique des fichiers PAC.")
        return False


def _test_proxy_auth_required(url: str, proxy_host: str) -> bool:
    """
    Teste si un proxy nécessite une authentification en effectuant une requête de test.
    
    Args:
        url: URL à tester
        proxy_host: Hôte proxy à utiliser (format: host:port)
        
    Returns:
        True si le proxy nécessite une authentification, False sinon
    """
    try:
        import requests
        from requests.exceptions import ProxyError
        
        # Configuration du proxy sans authentification
        proxies = {
            "http": f"http://{proxy_host}",
            "https": f"http://{proxy_host}"
        }
        
        # Tenter une requête avec un timeout court
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            return False  # Si la requête réussit, pas besoin d'authentification
        except ProxyError as e:
            # Vérifier si l'erreur est due à un 407 (Proxy Authentication Required)
            error_str = str(e)
            if "407" in error_str or "Proxy Authentication Required" in error_str:
                logger.debug(f"Le proxy PAC nécessite une authentification")
                return True
        except Exception as e:
            logger.debug(f"Erreur lors du test d'authentification proxy: {e}")
    except ImportError:
        logger.debug("Le module requests n'est pas disponible pour tester l'authentification proxy")
    
    # Par défaut, supposer qu'aucune authentification n'est requise
    return False


def _get_proxy_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Demande à l'utilisateur de saisir ses identifiants proxy.
    
    Returns:
        Tuple (nom d'utilisateur, mot de passe)
    """
    import getpass
    
    try:
        # D'abord, essayer de récupérer depuis les variables d'environnement
        username = os.environ.get("PROXY_USERNAME")
        password = os.environ.get("PROXY_PASSWORD")
        
        # Si non disponible, demander interactivement
        if not username:
            username = input("Nom d'utilisateur proxy PAC: ")
        
        if not password:
            password = getpass.getpass("Mot de passe proxy PAC: ")
            
        return username, password
    except Exception as e:
        logger.debug(f"Erreur lors de la récupération des identifiants: {e}")
        return None, None
