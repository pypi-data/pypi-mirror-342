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


def _get_pac_proxy(url: str, pac_url: Optional[str] = None) -> Dict[str, str]:
    """
    Fonction interne pour obtenir la configuration de proxy à partir d'un PAC.
    Cette fonction est séparée pour faciliter les tests.
    """
    proxy_config = {}
    
    try:
        # Importer le module pypac s'il est disponible
        if is_pac_available():
            import pypac
            from pypac import PACSession
            from pypac.parser import PACFile
            
            # Utiliser pypac pour analyser le fichier PAC
            if pac_url:
                # Si une URL PAC est spécifiée explicitement
                parsed_pac = PACFile.from_url(pac_url)
                proxy_str = parsed_pac.find_proxy_for_url(url, urlparse(url).netloc)
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
    
    return proxy_config


def get_proxy_for_url(url: str, pac_url: Optional[str] = None) -> Dict[str, str]:
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
    proxy_config = _get_pac_proxy(url, pac_url)
    
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
        return False
