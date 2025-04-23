"""
Module gérant la sécurisation et le masquage des mots de passe dans les configurations de proxy.
"""

import re
from typing import Dict, Any, Union


class SecureProxyConfig:
    """
    Classe encapsulant une configuration de proxy avec masquage des mots de passe.
    
    Cette classe permet d'utiliser une configuration de proxy normalement, tout en
    masquant automatiquement les mots de passe lors de l'affichage, du débogage ou
    de la journalisation, afin d'éviter les fuites accidentelles d'informations.
    """
    
    def __init__(self, proxy_config: Dict[str, str]) -> None:
        """
        Initialise une configuration de proxy sécurisée.
        
        Args:
            proxy_config: Dictionnaire de configuration de proxy (http/https/etc.)
        """
        self._proxy_config = proxy_config
    
    def get_config(self) -> Dict[str, str]:
        """
        Retourne la configuration de proxy non masquée pour une utilisation réelle.
        
        Returns:
            La configuration de proxy complète avec mots de passe en clair
        """
        return self._proxy_config
    
    def __getitem__(self, key: str) -> str:
        """
        Permet d'accéder à la configuration comme un dictionnaire.
        
        Args:
            key: Clé de configuration (http/https/etc.)
            
        Returns:
            La valeur associée à la clé
        """
        return self._proxy_config[key]
    
    def __contains__(self, key: str) -> bool:
        """
        Vérifie si une clé existe dans la configuration.
        
        Args:
            key: Clé à vérifier
            
        Returns:
            True si la clé existe, False sinon
        """
        return key in self._proxy_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration avec valeur par défaut.
        
        Args:
            key: Clé de configuration
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            La valeur associée à la clé ou la valeur par défaut
        """
        return self._proxy_config.get(key, default)
    
    def __repr__(self) -> str:
        """
        Représentation sécurisée de la configuration avec mots de passe masqués.
        
        Returns:
            La représentation de l'objet avec mots de passe masqués par des '*'
        """
        return f"SecureProxyConfig({self._mask_passwords(str(self._proxy_config))})"
    
    def __str__(self) -> str:
        """
        Représentation texte sécurisée avec mots de passe masqués.
        
        Returns:
            La représentation texte avec mots de passe masqués
        """
        return self._mask_passwords(str(self._proxy_config))
    
    @staticmethod
    def _mask_passwords(text: str) -> str:
        """
        Masque les mots de passe dans une chaîne de texte.
        
        Args:
            text: Texte potentiellement contenant des mots de passe
            
        Returns:
            Le texte avec les mots de passe remplacés par '********'
        """
        # Recherche les URLs avec authentification de la forme http(s)://user:password@host
        # Pattern pour trouver les configurations avec des mots de passe
        pattern = r'([\'\"]?[^:]+[\'\"]?\s*:\s*[\'\"]?https?://[^:]+:)([^@\'\"\s]+)([@\'\"\s])'

        def replace_passwords(match):
            # Remplace le mot de passe par des asterisques, en préservant la structure
            return f"{match.group(1)}********{match.group(3)}"

        return re.sub(pattern, replace_passwords, text, flags=re.DOTALL)
    
    def keys(self):
        """
        Retourne les clés de la configuration.
        
        Returns:
            Les clés de la configuration (http/https/etc.)
        """
        return self._proxy_config.keys()
    
    def items(self):
        """
        Retourne les paires clé-valeur de la configuration.
        
        Returns:
            Les paires clé-valeur avec mots de passe en clair
        """
        return self._proxy_config.items()
    
    def values(self):
        """
        Retourne les valeurs de la configuration.
        
        Returns:
            Les valeurs de la configuration avec mots de passe en clair
        """
        return self._proxy_config.values()
    
    def copy(self) -> Dict[str, str]:
        """
        Retourne une copie de la configuration.
        
        Returns:
            Une copie du dictionnaire de configuration
        """
        return self._proxy_config.copy()


def mask_password_in_url(url: Union[str, None]) -> str:
    """
    Masque le mot de passe dans une URL de proxy.
    
    Args:
        url: URL de proxy potentiellement avec authentification
        
    Returns:
        L'URL avec mot de passe masqué ou l'URL originale si pas d'authentification
    """
    if not url:
        return ""
        
    pattern = r'(https?://[^:]+:)([^@]+)(@[^/]+)'
    return re.sub(pattern, r'\1********\3', url)
