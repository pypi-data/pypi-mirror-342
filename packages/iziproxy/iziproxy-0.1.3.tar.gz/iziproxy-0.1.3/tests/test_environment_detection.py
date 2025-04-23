"""
Tests pour les fonctionnalités de détection d'environnement.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import socket
from iziproxy.proxy_ninja import IziProxy


class TestEnvironmentDetection(unittest.TestCase):
    """
    Tests unitaires pour les méthodes de détection d'environnement.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Sauvegarder les variables d'environnement
        self.original_env = {}
        for key in ['ENVIRONMENT', 'ENV', 'APP_ENV']:
            self.original_env[key] = os.environ.get(key)
            if key in os.environ:
                del os.environ[key]
    
    def tearDown(self):
        """
        Nettoyage après chaque test.
        """
        # Restaurer les variables d'environnement
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
    
    def test_detect_environment_default(self):
        """
        Teste la détection d'environnement par défaut (sans configuration).
        """
        ninja = IziProxy()
        # Par défaut, l'environnement devrait être "local"
        self.assertEqual(ninja.environment, "local")
    
    @patch('socket.gethostname')
    def test_detect_environment_hostname_direct_match(self, mock_hostname):
        """
        Teste la détection d'environnement par nom d'hôte avec correspondance directe.
        """
        # Configurer le hostname à retourner
        mock_hostname.return_value = "dev-machine-123"
        
        # Configurer IziProxy avec détection par hostname
        config = {
            "environment_detection": {
                "method": "hostname",
                "hostname_patterns": {
                    "local": ["local-pc", "laptop"],
                    "dev": ["dev-machine", "dev-server"],
                    "prod": ["prod-server"]
                }
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # Le hostname contient "dev-machine", donc l'environnement devrait être "dev"
            self.assertEqual(env, "dev")
    
    @patch('socket.gethostname')
    def test_detect_environment_hostname_regex(self, mock_hostname):
        """
        Teste la détection d'environnement par nom d'hôte avec regex.
        """
        # Configurer le hostname à retourner
        mock_hostname.return_value = "prod-srv-42"
        
        # Configurer IziProxy avec détection par regex
        config = {
            "environment_detection": {
                "method": "hostname",
                "hostname_regex": {
                    "local": ["^dev-\\w+-\\d+$", "^laptop-\\d+$"],
                    "dev": ["^staging-\\w+$"],
                    "prod": ["^prod-srv-\\d+$"]
                }
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # Le hostname correspond au regex "^prod-srv-\\d+$", donc l'environnement devrait être "prod"
            self.assertEqual(env, "prod")
    
    def test_detect_environment_env_var_simple(self):
        """
        Teste la détection d'environnement par variable d'environnement (cas simple).
        """
        # Configurer la variable d'environnement
        os.environ['ENVIRONMENT'] = 'production'
        
        # Configurer IziProxy avec détection par variable d'environnement
        config = {
            "environment_detection": {
                "method": "env_var",
                "env_var_name": "ENVIRONMENT"
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # La variable contient "production", donc l'environnement devrait être "prod"
            self.assertEqual(env, "prod")
    
    def test_detect_environment_multiple_env_vars(self):
        """
        Teste la détection d'environnement avec plusieurs variables d'environnement.
        """
        # Configurer plusieurs variables d'environnement
        os.environ['APP_ENV'] = 'dev'
        # Définir explicitement ENVIRONMENT pour s'assurer que IziProxy la détecte
        os.environ['ENVIRONMENT'] = 'development'
        
        # Configurer IziProxy avec détection par plusieurs variables
        config = {
            "environment_detection": {
                "method": "env_var",
                "env_var_names": ["ENV", "ENVIRONMENT", "APP_ENV"]
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # L'environnement détecté devrait être "dev" à partir de ENVIRONMENT
            self.assertEqual(env, "dev")
    
    @patch('socket.socket')
    def test_detect_environment_by_ip(self, mock_socket):
        """
        Teste la détection d'environnement par adresse IP.
        """
        # Configurer le mock pour simuler une adresse IP spécifique
        mock_socket_instance = MagicMock()
        mock_socket_instance.getsockname.return_value = ["192.168.1.123"]
        mock_socket.return_value = mock_socket_instance
        
        # Configurer IziProxy avec détection par IP
        config = {
            "environment_detection": {
                "method": "ip",
                "ip_ranges": {
                    "local": ["127.0.0.", "192.168.1."],
                    "dev": ["10.0.1."],
                    "prod": ["10.1.1."]
                }
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # L'IP commence par "192.168.1.", donc l'environnement devrait être "local"
            self.assertEqual(env, "local")
    
    @patch('builtins.input')
    def test_detect_environment_ask(self, mock_input):
        """
        Teste la détection d'environnement interactivement.
        """
        # Configurer le mock pour simuler l'entrée utilisateur
        mock_input.return_value = "3"  # Choix "Production"
        
        # Configurer IziProxy avec détection interactive
        config = {
            "environment_detection": {
                "method": "ask"
            }
        }
        
        # Créer une instance avec le mock de configuration
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            ninja = IziProxy()
            ninja.config = config
            env = ninja._detect_environment()
            
            # L'entrée "3" correspond à "Production", donc l'environnement devrait être "prod"
            self.assertEqual(env, "prod")


if __name__ == "__main__":
    unittest.main()