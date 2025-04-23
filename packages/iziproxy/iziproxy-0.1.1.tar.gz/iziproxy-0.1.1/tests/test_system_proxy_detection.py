"""
Tests pour les fonctionnalités de détection de proxy système.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import platform
import sys
from iziproxy.proxy_ninja import IziProxy


class TestSystemProxyDetection(unittest.TestCase):
    """
    Tests unitaires pour les méthodes de détection de proxy système.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Sauvegarder les variables d'environnement
        self.original_env = {}
        for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'no_proxy']:
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
    
    def test_get_env_proxy_config_uppercase(self):
        """
        Teste la récupération de configuration proxy depuis variables d'environnement majuscules.
        """
        # Configurer les variables d'environnement
        os.environ['HTTP_PROXY'] = 'http://proxy-upper.example.com:8080'
        os.environ['HTTPS_PROXY'] = 'http://proxy-upper.example.com:8443'
        os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
        
        ninja = IziProxy()
        config = ninja._get_env_proxy_config()
        
        # Vérifier que les variables d'environnement majuscules sont utilisées
        self.assertEqual(config['http'], 'http://proxy-upper.example.com:8080')
        self.assertEqual(config['https'], 'http://proxy-upper.example.com:8443')
    
    def test_get_env_proxy_config_lowercase(self):
        """
        Teste la récupération de configuration proxy depuis variables d'environnement minuscules.
        """
        # Configurer les variables d'environnement
        os.environ['http_proxy'] = 'http://proxy-lower.example.com:8080'
        os.environ['https_proxy'] = 'http://proxy-lower.example.com:8443'
        os.environ['no_proxy'] = 'localhost,127.0.0.1'
        
        ninja = IziProxy()
        config = ninja._get_env_proxy_config()
        
        # Vérifier que les variables d'environnement minuscules sont utilisées
        self.assertEqual(config['http'], 'http://proxy-lower.example.com:8080')
        self.assertEqual(config['https'], 'http://proxy-lower.example.com:8443')
    
    def test_get_env_proxy_config_precedence(self):
        """
        Teste la priorité des variables d'environnement (majuscules vs minuscules).
        """
        # Configurer les variables d'environnement
        os.environ['HTTP_PROXY'] = 'http://proxy-upper.example.com:8080'
        os.environ['http_proxy'] = 'http://proxy-lower.example.com:8080'
        
        ninja = IziProxy()
        config = ninja._get_env_proxy_config()
        
        # Vérifier l'ordre dans lequel les variables sont recherchées
        # Note: Adapter le test en fonction de l'implémentation réelle
        self.assertIn('http', config)
        self.assertEqual(config['http'], os.environ['HTTP_PROXY'])
    
    @unittest.skipIf(platform.system() != "Windows", "Test spécifique à Windows")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_get_system_proxy_config_windows_simple(self, mock_query_value, mock_open_key):
        """
        Teste la récupération de configuration proxy depuis le registre Windows (cas simple).
        """
        # Configurer les mocks pour simuler le registre Windows
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        # Simuler ProxyEnable = 1 et ProxyServer = simple server:port
        mock_query_value.side_effect = lambda key, name: {
            "ProxyEnable": (1, 1),
            "ProxyServer": ("proxy.windows.example.com:8080", 1)
        }[name]
        
        ninja = IziProxy()
        config = ninja._get_system_proxy_config()
        
        # Vérifier que le proxy du registre est utilisé pour http et https
        self.assertEqual(config['http'], 'http://proxy.windows.example.com:8080')
        self.assertEqual(config['https'], 'http://proxy.windows.example.com:8080')
    
    @unittest.skipIf(platform.system() != "Windows", "Test spécifique à Windows")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_get_system_proxy_config_windows_protocol_specific(self, mock_query_value, mock_open_key):
        """
        Teste la récupération de configuration proxy depuis le registre Windows (avec protocoles spécifiques).
        """
        # Configurer les mocks pour simuler le registre Windows
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        # Simuler ProxyEnable = 1 et ProxyServer avec des protocoles spécifiques
        mock_query_value.side_effect = lambda key, name: {
            "ProxyEnable": (1, 1),
            "ProxyServer": ("http=proxy-http.windows.example.com:8080;https=proxy-https.windows.example.com:8443", 1)
        }[name]
        
        ninja = IziProxy()
        config = ninja._get_system_proxy_config()
        
        # Vérifier que les proxys spécifiques à chaque protocole sont utilisés
        self.assertEqual(config['http'], 'http://proxy-http.windows.example.com:8080')
        self.assertEqual(config['https'], 'http://proxy-https.windows.example.com:8443')
    
    @unittest.skipIf(platform.system() != "Windows", "Test spécifique à Windows")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_get_system_proxy_config_windows_disabled(self, mock_query_value, mock_open_key):
        """
        Teste la récupération de configuration proxy depuis le registre Windows (proxy désactivé).
        """
        # Configurer les mocks pour simuler le registre Windows
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        # Simuler ProxyEnable = 0 (désactivé)
        mock_query_value.side_effect = lambda key, name: {
            "ProxyEnable": (0, 1),
            "ProxyServer": ("proxy.windows.example.com:8080", 1)
        }[name]
        
        ninja = IziProxy()
        config = ninja._get_system_proxy_config()
        
        # Vérifier que aucun proxy n'est retourné (dict vide)
        self.assertEqual(config, {})
    
    @patch('iziproxy.pac_utils.get_proxy_for_url')
    @patch('iziproxy.pac_utils.detect_system_pac_url')
    @patch('iziproxy.pac_utils.is_pac_available')
    def test_get_proxy_config_priority_direct(self, mock_is_pac_available, 
                                             mock_detect_pac, mock_get_proxy):
        """
        Teste la priorité des sources de configuration (cas direct).
        """
        # Configurer les variables d'environnement
        os.environ['HTTP_PROXY'] = 'http://proxy-env.example.com:8080'
        
        # Configurer les mocks
        mock_is_pac_available.return_value = True
        mock_detect_pac.return_value = "http://pac.example.com/proxy.pac"
        mock_get_proxy.return_value = {
            "http": "http://proxy-pac.example.com:8080", 
            "https": "http://proxy-pac.example.com:8080"
        }
        
        # Créer une instance avec configuration directe
        ninja = IziProxy(proxy_url="http://proxy-direct.example.com:8080")
        config = ninja.get_proxy_config()
        
        # Vérifier que la configuration directe a priorité
        self.assertIn("proxy-direct.example.com", str(config))
        
        # Vérifier que les autres méthodes n'ont pas été utilisées
        mock_get_proxy.assert_not_called()
    
    @patch('iziproxy.pac_utils.get_proxy_for_url')
    @patch('iziproxy.pac_utils.detect_system_pac_url')
    @patch('iziproxy.pac_utils.is_pac_available')
    def test_get_proxy_config_priority_env(self, mock_is_pac_available, 
                                          mock_detect_pac, mock_get_proxy):
        """
        Teste la priorité des sources de configuration (cas variables d'environnement).
        """
        # Configurer les variables d'environnement
        os.environ['HTTP_PROXY'] = 'http://proxy-env.example.com:8080'
        
        # Configurer les mocks
        mock_is_pac_available.return_value = True
        mock_detect_pac.return_value = "http://pac.example.com/proxy.pac"
        mock_get_proxy.return_value = {
            "http": "http://proxy-pac.example.com:8080", 
            "https": "http://proxy-pac.example.com:8080"
        }
        
        # Créer une instance sans configuration directe
        ninja = IziProxy()
        config = ninja.get_proxy_config()
        
        # Vérifier que la configuration de l'environnement a priorité sur PAC
        self.assertIn("proxy-env.example.com", str(config))
        
        # Vérifier que le PAC n'a pas été utilisé
        mock_get_proxy.assert_not_called()
    
    @patch('iziproxy.proxy_ninja.get_proxy_for_url')
    def test_get_proxy_config_priority_pac(self, mock_get_proxy):
        """
        Teste la priorité des sources de configuration (cas PAC).
        """
        # Configurer le mock pour retourner une configuration de proxy spécifique
        expected_proxy = {
            "http": "http://proxy-pac.example.com:8080", 
            "https": "http://proxy-pac.example.com:8080"
        }
        mock_get_proxy.return_value = expected_proxy
        
        # S'assurer qu'aucune variable d'environnement n'est définie
        for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
            if var in os.environ:
                del os.environ[var]
        
        # Créer une instance avec uniquement le PAC comme source valide
        with patch('iziproxy.proxy_ninja.is_pac_available', return_value=True):
            with patch('iziproxy.proxy_ninja.detect_system_pac_url', return_value="http://pac.example.com/proxy.pac"):
                # Créer l'instance IziProxy sans proxy direct
                ninja = IziProxy()
                
                # Remplacer l'attribut direct_proxy_config pour qu'il soit vide
                ninja.direct_proxy_config = {}
                
                # Remplacer config pour qu'il n'y ait pas de config YAML
                ninja.config = {}
                
                # Mocker les méthodes de détection de proxy
                with patch.object(ninja, '_get_env_proxy_config', return_value={}):
                    with patch.object(ninja, '_get_system_proxy_config', return_value={}):
                        # Manuellement définir pac_url pour s'assurer que la détection PAC est utilisée
                        ninja.pac_url = "http://pac.example.com/proxy.pac"
                        
                        # Maintenant, get_proxy_config() devrait utiliser PAC comme seule source
                        config = ninja.get_proxy_config()
                        
                        # Vérifier que le PAC a été utilisé
                        mock_get_proxy.assert_called_once()
                        
                        # Vérifier la configuration finale
                        self.assertEqual(expected_proxy, dict(config.get_config()))


if __name__ == "__main__":
    unittest.main()