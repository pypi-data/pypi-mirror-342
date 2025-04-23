"""
Tests pour la classe principale IziProxy.
"""

import unittest
import os
import socket
import platform
from unittest.mock import patch, MagicMock, mock_open
import tempfile
from iziproxy.proxy_ninja import IziProxy
from iziproxy.secure_password import SecureProxyConfig


class TestIziProxy(unittest.TestCase):
    """
    Tests unitaires pour la classe principale IziProxy.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Créer un dictionnaire pour stocker les variables d'environnement originales
        self.original_env = {}
        for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'no_proxy']:
            self.original_env[key] = os.environ.get(key)
        
        # Nettoyer les variables d'environnement pour les tests
        for key in self.original_env:
            if key in os.environ:
                del os.environ[key]
    
    def tearDown(self):
        """
        Nettoyage après chaque test.
        """
        # Restaurer les variables d'environnement originales
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
    
    def test_init_without_config(self):
        """
        Teste l'initialisation sans configuration explicite.
        """
        proxy = IziProxy()
        self.assertIsNotNone(proxy.environment)
        self.assertIsNotNone(proxy.config)
    
    def test_init_with_explicit_params(self):
        """
        Teste l'initialisation avec paramètres explicites.
        """
        proxy = IziProxy(
            environment="prod",
            proxy_url="http://proxy.example.com:8080",
            username="user",
            password="pass"
        )
        
        self.assertEqual(proxy.environment, "prod")
        self.assertIsNotNone(proxy.direct_proxy_config)
        self.assertIn("http", proxy.direct_proxy_config)
        self.assertIn("https", proxy.direct_proxy_config)
    
    def test_load_config_file(self):
        """
        Teste le chargement d'un fichier de configuration.
        """
        # Créer un fichier de configuration temporaire
        config_content = """
        environments:
          local:
            proxy_url: http://proxy.local.example.com:8080
            requires_auth: true
          prod:
            proxy_url: http://proxy.prod.example.com:8080
            requires_auth: false
        """
        
        # Utiliser mock_open pour simuler le fichier
        with patch('builtins.open', mock_open(read_data=config_content)):
            proxy = IziProxy(config_file="dummy_path.yaml")
            
            # Vérifier que la configuration a été chargée
            self.assertIn("environments", proxy.config)
            self.assertIn("local", proxy.config["environments"])
            self.assertIn("prod", proxy.config["environments"])
    
    @patch("socket.gethostname")
    def test_detect_environment_hostname(self, mock_hostname):
        """
        Teste la détection d'environnement par nom d'hôte.
        """
        # Configuration avec détection par nom d'hôte
        config = {
            "environment_detection": {
                "method": "hostname",
                "hostname_patterns": {
                    "local": ["laptop", "dev-pc"],
                    "prod": ["prod-server"]
                }
            }
        }
        
        # Test avec nom d'hôte de production
        mock_hostname.return_value = "prod-server-01"
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            proxy = IziProxy()
            proxy.config = config
            env = proxy._detect_environment()
            self.assertEqual(env, "prod")
        
        # Test avec nom d'hôte de développement
        mock_hostname.return_value = "laptop-user"
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            proxy = IziProxy()
            proxy.config = config
            env = proxy._detect_environment()
            self.assertEqual(env, "local")
    
    @patch.dict(os.environ, {"ENVIRONMENT": "production"})
    def test_detect_environment_env_var(self):
        """
        Teste la détection d'environnement par variable d'environnement.
        """
        # Configuration avec détection par variable d'environnement
        config = {
            "environment_detection": {
                "method": "env_var",
                "env_var_name": "ENVIRONMENT"
            }
        }
        
        with patch.object(IziProxy, "_load_config_file", return_value=None):
            proxy = IziProxy()
            proxy.config = config
            env = proxy._detect_environment()
            self.assertEqual(env, "prod")
    
    def test_get_proxy_config_direct(self):
        """
        Teste get_proxy_config avec configuration directe.
        """
        proxy = IziProxy(
            proxy_url="http://direct.example.com:8080",
            username="user",
            password="pass"
        )
        
        config = proxy.get_proxy_config()
        
        # Vérifier que le résultat est de type SecureProxyConfig
        self.assertIsInstance(config, SecureProxyConfig)
        
        # Vérifier que la configuration contient les URLs de proxy
        self.assertIn("http", config)
        self.assertIn("https", config)
        
        # Vérifier que les identifiants sont intégrés
        self.assertIn("user:pass@", config["http"])
    
    @patch.dict(os.environ, {"HTTP_PROXY": "http://env.example.com:8080"})
    def test_get_proxy_config_from_env(self):
        """
        Teste get_proxy_config avec configuration depuis variables d'environnement.
        """
        proxy = IziProxy()
        config = proxy.get_proxy_config()
        
        # Vérifier que le proxy des variables d'environnement est utilisé
        self.assertEqual(config["http"], "http://env.example.com:8080")
    
    @patch('requests.Session')
    def test_configure_session(self, mock_session):
        """
        Teste la configuration d'une session requests.
        """
        # Créer une session mock
        session = MagicMock()
        session.proxies = {}
        
        # Configurer IziProxy avec un proxy direct
        proxy = IziProxy(proxy_url="http://example.com:8080")
        
        # Configurer la session
        proxy.configure_session(session)
        
        # Vérifier que les proxies ont été configurés
        self.assertIn("http", session.proxies)
        self.assertIn("https", session.proxies)
    
    def test_build_proxy_config(self):
        """
        Teste la construction de configuration de proxy.
        """
        proxy = IziProxy()
        
        # Test sans authentification
        config = proxy._build_proxy_config("http://example.com:8080")
        self.assertEqual(config["http"], "http://example.com:8080")
        self.assertEqual(config["https"], "http://example.com:8080")
        
        # Test avec authentification
        config = proxy._build_proxy_config("http://example.com:8080", "user", "pass")
        self.assertEqual(config["http"], "http://user:pass@example.com:8080")
        self.assertEqual(config["https"], "http://user:pass@example.com:8080")
        
        # Test avec URL contenant déjà des identifiants
        config = proxy._build_proxy_config("http://user:oldpass@example.com:8080", "newuser", "newpass")
        self.assertIn("newuser:newpass@", config["http"])
    
    @patch('keyring.get_password')
    @patch('keyring.set_password')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_get_credentials(self, mock_input, mock_getpass, mock_set_password, mock_get_password):
        """
        Teste la récupération des identifiants.
        """
        proxy = IziProxy()
        
        # Configurer les mocks
        mock_input.return_value = "user_input"
        mock_getpass.return_value = "pass_input"
        mock_get_password.return_value = None  # Pas de mot de passe stocké
        
        # Tester sans identifiants prédéfinis
        username, password = proxy._get_credentials()
        
        # Vérifier que l'entrée utilisateur a été utilisée
        self.assertEqual(username, "user_input")
        self.assertEqual(password, "pass_input")
        
        # Vérifier que les identifiants ont été stockés
        mock_set_password.assert_called()
    
    @patch.dict(os.environ, {"HTTP_PROXY": "http://env.example.com:8080", "HTTPS_PROXY": "http://env.example.com:8443"})
    def test_get_env_proxy_config(self):
        """
        Teste la récupération de configuration proxy depuis les variables d'environnement.
        """
        proxy = IziProxy()
        config = proxy._get_env_proxy_config()
        
        self.assertEqual(config["http"], "http://env.example.com:8080")
        self.assertEqual(config["https"], "http://env.example.com:8443")
    
    @unittest.skipIf(platform.system() != "Windows", "Test spécifique à Windows")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_get_system_proxy_config_windows(self, mock_query_value, mock_open_key):
        """
        Teste la récupération de configuration proxy depuis le registre Windows.
        """
        # Configurer les mocks pour simuler un proxy actif dans le registre
        mock_open_key.return_value.__enter__.return_value = MagicMock()
        
        # Simuler ProxyEnable = 1 (activé)
        # Simuler ProxyServer = "proxy.example.com:8080"
        mock_query_value.side_effect = [
            (1, 1),  # ProxyEnable
            ("proxy.example.com:8080", 1)  # ProxyServer
        ]
        
        proxy = IziProxy()
        config = proxy._get_system_proxy_config()
        
        self.assertIn("http", config)
        self.assertIn("https", config)
        self.assertEqual(config["http"], "http://proxy.example.com:8080")
    
    @patch('requests.get')
    def test_test_connection(self, mock_get):
        """
        Teste la méthode de test de connexion.
        """
        # Configurer le mock pour simuler une réponse réussie
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        proxy = IziProxy(proxy_url="http://example.com:8080")
        result = proxy.test_connection()
        
        self.assertTrue(result)
        mock_get.assert_called_once()
    
    def test_get_current_environment(self):
        """
        Teste la méthode get_current_environment.
        """
        proxy = IziProxy(environment="test")
        self.assertEqual(proxy.get_current_environment(), "test")
    
    @patch('iziproxy.proxy_ninja.IziProxy.test_connection')
    @patch('iziproxy.proxy_ninja.detect_system_pac_url')
    @patch('iziproxy.proxy_ninja.is_pac_available')
    def test_get_proxy_info(self, mock_is_pac_available, mock_detect_pac, mock_test_connection):
        """
        Teste la méthode get_proxy_info.
        """
        # Configurer les mocks
        mock_is_pac_available.return_value = True
        mock_detect_pac.return_value = "http://pac.example.com/proxy.pac"
        mock_test_connection.return_value = True

        # Définir explicitement l'URL PAC lors de l'initialisation
        proxy = IziProxy(
            environment="test",
            proxy_url="http://example.com:8080",
            pac_url="http://pac.example.com/proxy.pac"
        )
        info = proxy.get_proxy_info()

        self.assertEqual(info["environment"], "test")
        self.assertTrue(info["proxy_working"])
        self.assertEqual(info["pac_url"], "http://pac.example.com/proxy.pac")
        self.assertTrue(info["pac_support_available"])


if __name__ == "__main__":
    unittest.main()
