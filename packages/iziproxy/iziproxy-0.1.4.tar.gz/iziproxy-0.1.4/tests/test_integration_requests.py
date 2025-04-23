"""
Tests d'intégration avec la bibliothèque requests.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from iziproxy.proxy_ninja import IziProxy
from iziproxy.secure_password import SecureProxyConfig


class TestRequestsIntegration(unittest.TestCase):
    """
    Tests d'intégration avec la bibliothèque requests.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Sauvegarder les variables d'environnement
        self.original_env = {}
        for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY']:
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
    
    @patch('requests.Session')
    def test_configure_session(self, mock_session_class):
        """
        Teste la configuration d'une session requests.
        """
        # Créer une session mock
        mock_session = MagicMock()
        mock_session.proxies = {}
        mock_session_class.return_value = mock_session
        
        # Configurer IziProxy avec un proxy explicite
        ninja = IziProxy(proxy_url="http://proxy.test.com:8080")
        
        # Configurer la session
        session = requests.Session()
        ninja.configure_session(session)
        
        # Vérifier que les proxies ont été configurés correctement
        self.assertIn("http", session.proxies)
        self.assertIn("https", session.proxies)
        self.assertEqual(session.proxies["http"], "http://proxy.test.com:8080")
    
    @patch('requests.Session')
    def test_configure_session_with_auth(self, mock_session_class):
        """
        Teste la configuration d'une session requests avec authentification.
        """
        # Créer une session mock
        mock_session = MagicMock()
        mock_session.proxies = {}
        mock_session_class.return_value = mock_session
        
        # Configurer IziProxy avec un proxy et authentification
        ninja = IziProxy(
            proxy_url="http://proxy.test.com:8080",
            username="testuser",
            password="testpass"
        )
        
        # Configurer la session
        session = requests.Session()
        ninja.configure_session(session)
        
        # Vérifier que les proxies avec authentification ont été configurés
        self.assertIn("http", session.proxies)
        self.assertIn("https", session.proxies)
        self.assertIn("testuser:testpass@", session.proxies["http"])
    
    @patch('requests.Session')
    def test_configure_session_ssl_verification(self, mock_session_class):
        """
        Teste la configuration de la vérification SSL dans une session requests.
        """
        # Créer une session mock
        mock_session = MagicMock()
        mock_session.proxies = {}
        mock_session_class.return_value = mock_session
        
        # Configurer IziProxy avec verify_ssl = False
        ninja = IziProxy(proxy_url="http://proxy.test.com:8080")
        
        # Modifier la configuration pour désactiver la vérification SSL
        ninja.config = {
            "environments": {
                "local": {
                    "verify_ssl": False
                }
            }
        }
        ninja.environment = "local"
        
        # Configurer la session
        session = requests.Session()
        ninja.configure_session(session)
        
        # Vérifier que la vérification SSL a été désactivée
        self.assertFalse(session.verify)
    
    @patch('requests.get')
    def test_direct_use_with_requests(self, mock_get):
        """
        Teste l'utilisation directe avec requests.get().
        """
        # Configurer la réponse mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Configurer IziProxy
        ninja = IziProxy(proxy_url="http://proxy.test.com:8080")
        
        # Utiliser directement avec requests.get()
        response = requests.get(
            "https://api.example.com/data",
            proxies=ninja.get_proxy_config()
        )
        
        # Vérifier que la requête a été faite avec les bons paramètres
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://api.example.com/data")
        self.assertIsInstance(kwargs["proxies"], SecureProxyConfig)
    
    @patch('requests.get')
    def test_test_connection(self, mock_get):
        """
        Teste la méthode test_connection().
        """
        # Configurer la réponse mock pour un succès
        mock_success = MagicMock()
        mock_success.status_code = 200
        
        # Configurer la réponse mock pour un échec
        mock_failure = MagicMock()
        mock_failure.status_code = 500
        
        # Configurer le mock pour retourner différentes réponses
        mock_get.side_effect = [mock_success, mock_failure]
        
        # Tester avec une configuration fonctionnelle
        ninja = IziProxy(proxy_url="http://working.proxy.com:8080")
        self.assertTrue(ninja.test_connection())
        
        # Tester avec une configuration non fonctionnelle
        ninja = IziProxy(proxy_url="http://broken.proxy.com:8080")
        self.assertFalse(ninja.test_connection())
    
    @patch('requests.get')
    def test_test_connection_exception(self, mock_get):
        """
        Teste la gestion des exceptions dans test_connection().
        """
        # Configurer le mock pour lever une exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        # Tester avec une configuration qui génère une exception
        ninja = IziProxy(proxy_url="http://invalid.proxy.com:8080")
        self.assertFalse(ninja.test_connection())


if __name__ == "__main__":
    unittest.main()