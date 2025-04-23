"""
Module principal pour la gestion intelligente des proxys.
"""

import os
import platform
import socket
import re
import logging
import yaml
from typing import Dict, Optional, List, Union, Any, Tuple
import getpass
from urllib.parse import urlparse, urlunparse

# Importer keyring avec gestion d'erreur - certains environnements peuvent ne pas le supporter
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

from .secure_password import SecureProxyConfig, mask_password_in_url
from .pac_utils import get_proxy_for_url, detect_system_pac_url, is_pac_available, PacNotAvailableError

logger = logging.getLogger(__name__)


class IziProxy:
    """
    Classe principale pour la détection et configuration automatique des proxys.
    
    Cette classe gère la détection d'environnement, la configuration des proxys,
    et la sécurisation des identifiants pour simplifier l'utilisation de proxys
    d'entreprise dans différents environnements.
    """
    
    # Environnements pris en charge
    ENV_LOCAL = "local"
    ENV_DEV = "dev"
    ENV_PROD = "prod"
    
    # Noms des variables d'environnement standard pour les proxys
    PROXY_ENV_VARS = {
        "http": ["HTTP_PROXY", "http_proxy"],
        "https": ["HTTPS_PROXY", "https_proxy"],
        "no_proxy": ["NO_PROXY", "no_proxy"]
    }
    
    # Nom par défaut du fichier de configuration
    DEFAULT_CONFIG_FILE = "iziproxy.yaml"
    
    def __init__(
        self, 
        config_file: Optional[str] = None,
        environment: Optional[str] = None,
        pac_url: Optional[str] = None,
        proxy_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        app_name: str = "iziproxy"
    ) -> None:
        """
        Initialise IziProxy avec détection automatique ou paramètres spécifiés.
        
        Args:
            config_file: Chemin vers le fichier de configuration YAML (facultatif)
            environment: Environnement à utiliser (local/dev/prod) (facultatif)
            pac_url: URL du fichier PAC à utiliser (facultatif)
            proxy_url: URL du proxy à utiliser directement (facultatif)
            username: Nom d'utilisateur pour l'authentification proxy (facultatif)
            password: Mot de passe pour l'authentification proxy (facultatif)
            app_name: Nom de l'application pour le stockage des identifiants (facultatif)
        """
        self.app_name = app_name
        self.config = {}
        self.environment = None
        self.pac_url = pac_url
        
        # Charger la configuration depuis le fichier si spécifié
        if config_file:
            self._load_config_file(config_file)
        else:
            # Chercher automatiquement le fichier de configuration
            default_locations = [
                os.path.join(os.getcwd(), self.DEFAULT_CONFIG_FILE),
                os.path.join(os.path.expanduser("~"), self.DEFAULT_CONFIG_FILE)
            ]
            for location in default_locations:
                if os.path.exists(location):
                    self._load_config_file(location)
                    break
        
        # Déterminer l'environnement si non spécifié
        self.environment = environment or self._detect_environment()
        logger.debug(f"Environnement détecté: {self.environment}")
        
        # Stocker les paramètres de connexion directe si fournis
        self.direct_proxy_config = {}
        if proxy_url:
            self.direct_proxy_config = self._build_proxy_config(proxy_url, username, password)
    
    def _load_config_file(self, config_file: str) -> None:
        """
        Charge la configuration depuis un fichier YAML.
        
        Args:
            config_file: Chemin vers le fichier de configuration YAML
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file) or {}
                logger.debug(f"Configuration chargée depuis {config_file}")
        except Exception as e:
            logger.warning(f"Erreur lors du chargement de la configuration: {e}")
            self.config = {}
    
    def _detect_environment(self) -> str:
        """
        Détecte automatiquement l'environnement d'exécution.
        
        Returns:
            L'environnement détecté (local/dev/prod)
        """
        # Vérifier si une méthode spécifique est définie dans la configuration
        detection_config = self.config.get("environment_detection", {})
        method = detection_config.get("method", "auto")
        
        if method == "env_var":
            # Détection par variable d'environnement
            env_var_name = detection_config.get("env_var_name", "ENVIRONMENT")
            env_value = os.environ.get(env_var_name, "").lower()
            
            if "prod" in env_value:
                return self.ENV_PROD
            elif "dev" in env_value:
                return self.ENV_DEV
            elif "local" in env_value:
                return self.ENV_LOCAL
                
        elif method == "hostname":
            # Détection par nom d'hôte
            hostname = socket.gethostname().lower()
            
            # Vérifier les correspondances directes
            patterns = detection_config.get("hostname_patterns", {})
            for env, hostnames in patterns.items():
                if isinstance(hostnames, list) and any(h.lower() in hostname for h in hostnames):
                    return env
            
            # Vérifier les expressions régulières
            regex_patterns = detection_config.get("hostname_regex", {})
            for env, regexes in regex_patterns.items():
                if isinstance(regexes, list) and any(re.search(r, hostname, re.IGNORECASE) for r in regexes):
                    return env
                    
        elif method == "ip":
            # Détection par adresse IP
            ip_ranges = detection_config.get("ip_ranges", {})
            try:
                # Récupérer l'adresse IP locale
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                
                # Vérifier les plages d'IP (implémentation très basique)
                for env, ranges in ip_ranges.items():
                    for ip_range in ranges:
                        if local_ip.startswith(ip_range):
                            return env
            except Exception as e:
                logger.debug(f"Erreur lors de la détection d'IP: {e}")
                
        elif method == "ask":
            # Demander l'environnement interactivement
            try:
                print("Quel environnement souhaitez-vous utiliser ?")
                print("1. Local")
                print("2. Développement")
                print("3. Production")
                choice = input("Entrez le numéro (1-3): ")
                
                if choice == "3":
                    return self.ENV_PROD
                elif choice == "2":
                    return self.ENV_DEV
                else:
                    return self.ENV_LOCAL
            except Exception as e:
                logger.debug(f"Erreur lors de la demande interactive: {e}")
        
        # Par défaut, retourner l'environnement local
        return self.ENV_LOCAL
    
    def get_proxy_config(self) -> SecureProxyConfig:
        """
        Récupère la configuration de proxy appropriée pour l'environnement actuel.
        
        Returns:
            Configuration de proxy sécurisée (avec masquage des mots de passe)
        """
        # Si une configuration directe a été fournie, l'utiliser
        if self.direct_proxy_config:
            return SecureProxyConfig(self.direct_proxy_config)
        
        # Rechercher dans l'ordre: fichier de config, variables d'environnement, PAC, système
        proxy_config = {}
        
        # 1. Fichier de configuration
        env_config = self.config.get("environments", {}).get(self.environment, {})
        if env_config:
            proxy_url = env_config.get("proxy_url")
            requires_auth = env_config.get("requires_auth", False)
            
            if proxy_url:
                username = None
                password = None
                
                if requires_auth:
                    # Récupérer les identifiants
                    username, password = self._get_credentials(
                        env_config.get("username"),
                        env_config.get("password")
                    )
                
                proxy_config = self._build_proxy_config(proxy_url, username, password)
        
        # 2. Variables d'environnement si aucune config trouvée
        if not proxy_config:
            proxy_config = self._get_env_proxy_config()
        
        # 3. Fichier PAC si disponible et aucune config trouvée
        if not proxy_config:
            try:
                # Utiliser l'URL PAC spécifiée ou détecter automatiquement
                pac_url = self.pac_url or detect_system_pac_url()
                if pac_url and is_pac_available():
                    # On ne peut pas déterminer le proxy sans URL cible, donc on utilise un site courant
                    # Dans un cas réel, on utiliserait l'URL de la requête
                    proxy_config = get_proxy_for_url("https://www.google.com", pac_url)
            except Exception as e:
                logger.debug(f"Erreur lors de l'utilisation du PAC: {e}")
        
        # 4. Configuration système en dernier recours
        if not proxy_config:
            proxy_config = self._get_system_proxy_config()
        
        return SecureProxyConfig(proxy_config)
    
    def configure_session(self, session) -> None:
        """
        Configure une session requests avec les paramètres proxy appropriés.
        
        Args:
            session: Session requests à configurer
        """
        proxy_config = self.get_proxy_config()
        session.proxies.update(proxy_config.get_config())
        
        # Configurer également la session pour ignorer les certificats si nécessaire
        env_config = self.config.get("environments", {}).get(self.environment, {})
        verify_ssl = env_config.get("verify_ssl", True)
        if not verify_ssl:
            session.verify = False
    
    def _build_proxy_config(
        self, 
        proxy_url: str, 
        username: Optional[str] = None, 
        password: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Construit une configuration de proxy avec authentification si nécessaire.
        
        Args:
            proxy_url: URL du proxy
            username: Nom d'utilisateur pour l'authentification (facultatif)
            password: Mot de passe pour l'authentification (facultatif)
            
        Returns:
            Dictionnaire de configuration de proxy
        """
        # Analyser l'URL pour vérifier si elle contient déjà des identifiants
        parsed_url = urlparse(proxy_url)
        base_url = proxy_url
        
        # Si l'URL contient déjà des identifiants, les extraire
        if parsed_url.username or parsed_url.password:
            netloc = f"{parsed_url.hostname}"
            if parsed_url.port:
                netloc += f":{parsed_url.port}"
            
            scheme = parsed_url.scheme
            base_url = f"{scheme}://{netloc}"
            
            # Récupérer les identifiants de l'URL si non fournis explicitement
            if not username:
                username = parsed_url.username
            if not password:
                password = parsed_url.password
        
        # Assembler l'URL finale avec authentification si nécessaire
        final_url = base_url
        if username and password:
            # Extraire les composants
            parsed = urlparse(base_url)
            netloc = parsed.netloc
            
            # Construire l'URL avec authentification
            auth_netloc = f"{username}:{password}@{netloc}"
            parts = list(parsed)
            parts[1] = auth_netloc  # netloc est à l'indice 1
            final_url = urlunparse(parts)
        
        # Retourner la configuration pour http et https
        return {
            "http": final_url,
            "https": final_url
        }
    
    def _get_credentials(
        self, 
        username: Optional[str] = None, 
        password: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Récupère les identifiants de proxy en utilisant plusieurs sources.
        
        Args:
            username: Nom d'utilisateur prédéfini (facultatif)
            password: Mot de passe prédéfini (facultatif)
            
        Returns:
            Tuple (nom d'utilisateur, mot de passe)
        """
        final_username = username
        final_password = password
        
        # Si les identifiants ne sont pas fournis, essayer de les récupérer
        if not final_username or not final_password:
            # Variables d'environnement
            if not final_username:
                final_username = os.environ.get("PROXY_USERNAME")
            if not final_password:
                final_password = os.environ.get("PROXY_PASSWORD")
            
            # Gestionnaire de mots de passe si disponible
            if KEYRING_AVAILABLE and (not final_username or not final_password):
                try:
                    service_name = f"{self.app_name}-{self.environment}"
                    
                    # Récupérer le nom d'utilisateur
                    if not final_username:
                        stored_username = keyring.get_password(service_name, "username")
                        if stored_username:
                            final_username = stored_username
                    
                    # Récupérer le mot de passe si le nom d'utilisateur est connu
                    if final_username and not final_password:
                        stored_password = keyring.get_password(service_name, final_username)
                        if stored_password:
                            final_password = stored_password
                except Exception as e:
                    logger.debug(f"Erreur lors de l'accès au keyring: {e}")
            
            # Demander interactivement en dernier recours
            if not final_username:
                try:
                    final_username = input("Nom d'utilisateur proxy: ")
                except Exception:
                    pass
                
            if final_username and not final_password:
                try:
                    final_password = getpass.getpass("Mot de passe proxy: ")
                    
                    # Enregistrer dans le keyring pour les utilisations futures
                    if KEYRING_AVAILABLE and final_username and final_password:
                        try:
                            service_name = f"{self.app_name}-{self.environment}"
                            keyring.set_password(service_name, "username", final_username)
                            keyring.set_password(service_name, final_username, final_password)
                        except Exception as e:
                            logger.debug(f"Erreur lors de l'enregistrement dans keyring: {e}")
                except Exception:
                    pass
        
        return final_username, final_password
    
    def _get_env_proxy_config(self) -> Dict[str, str]:
        """
        Récupère la configuration de proxy depuis les variables d'environnement.
        
        Returns:
            Dictionnaire de configuration de proxy
        """
        proxy_config = {}
        
        # Rechercher les variables d'environnement standard
        for protocol, var_names in self.PROXY_ENV_VARS.items():
            for var_name in var_names:
                if var_name in os.environ:
                    value = os.environ[var_name]
                    if protocol != "no_proxy":
                        proxy_config[protocol] = value
                    break
        
        return proxy_config
    
    def _get_system_proxy_config(self) -> Dict[str, str]:
        """
        Détecte la configuration de proxy au niveau du système d'exploitation.
        
        Returns:
            Dictionnaire de configuration de proxy
        """
        system = platform.system()
        proxy_config = {}
        
        try:
            if system == "Windows":
                import winreg
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
                ) as key:
                    # Vérifier si le proxy est activé
                    try:
                        proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
                        if proxy_enable:
                            # Récupérer le serveur proxy
                            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
                            if proxy_server:
                                # Le format peut être "server:port" ou "protocol=server:port;..."
                                if "=" in proxy_server:
                                    # Format avec protocoles séparés
                                    for part in proxy_server.split(";"):
                                        if "=" in part:
                                            protocol, server = part.split("=", 1)
                                            if protocol.lower() in ("http", "https"):
                                                proxy_config[protocol.lower()] = f"http://{server}"
                                else:
                                    # Format simple "server:port"
                                    proxy_config["http"] = f"http://{proxy_server}"
                                    proxy_config["https"] = f"http://{proxy_server}"
                    except (FileNotFoundError, OSError):
                        pass
                        
            elif system == "Darwin":  # macOS
                # Exécuter networksetup pour récupérer les proxys
                # Méthode simplifiée qui pourrait être améliorée
                pass
                
            elif system == "Linux":
                # Essayer de lire la configuration GNOME, KDE, etc.
                # Méthode simplifiée qui pourrait être améliorée
                pass
        except Exception as e:
            logger.debug(f"Erreur lors de la détection du proxy système: {e}")
        
        return proxy_config
    
    def test_connection(self, url: str = "https://www.google.com") -> bool:
        """
        Teste la connectivité avec la configuration proxy actuelle.
        
        Args:
            url: URL à tester
            
        Returns:
            True si la connexion fonctionne, False sinon
        """
        try:
            import requests
            proxy_config = self.get_proxy_config().get_config()
            
            # Désactiver les avertissements sur les certificats auto-signés
            requests.packages.urllib3.disable_warnings()
            
            # Tenter une connexion avec timeout réduit
            response = requests.get(url, proxies=proxy_config, timeout=5, verify=False)
            return response.status_code < 400
        except Exception as e:
            logger.debug(f"Erreur de test de connexion: {e}")
            return False
    
    def get_current_environment(self) -> str:
        """
        Renvoie l'environnement actuellement détecté.
        
        Returns:
            Nom de l'environnement actuel (local/dev/prod)
        """
        return self.environment
    
    def get_proxy_info(self) -> Dict[str, Any]:
        """
        Renvoie des informations détaillées sur la configuration proxy actuelle.
        
        Returns:
            Dictionnaire d'informations détaillées
        """
        proxy_config = self.get_proxy_config()
        
        info = {
            "environment": self.environment,
            "proxy_config": str(proxy_config),
            "proxy_working": self.test_connection(),
            "pac_url": self.pac_url or detect_system_pac_url(),
            "pac_support_available": is_pac_available(),
            "keyring_available": KEYRING_AVAILABLE,
        }
        
        return info