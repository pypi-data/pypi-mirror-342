"""
Tests pour le module pac_utils.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from iziproxy.pac_utils import get_proxy_for_url, detect_system_pac_url, clear_pac_cache, is_pac_available


class TestPacUtils(unittest.TestCase):
    """
    Tests unitaires pour les fonctionnalités de fichiers PAC.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Réinitialiser le cache pour des tests propres
        clear_pac_cache()
    
    def test_is_pac_available(self):
        """
        Teste la vérification de disponibilité du support PAC.
        """
        # Test avec pypac non disponible (simulé)
        with patch.dict('sys.modules', {'pypac': None}):
            # Forcer l'import à échouer
            if 'pypac' in sys.modules:
                sys.modules.pop('pypac')
            self.assertFalse(is_pac_available())
        
        # Test avec pypac disponible (simulé)
        mock_pypac = MagicMock()
        with patch.dict('sys.modules', {'pypac': mock_pypac}):
            self.assertTrue(is_pac_available())
    
    @patch('iziproxy.pac_utils.detect_system_pac_url')
    def test_get_proxy_for_url_no_pac(self, mock_detect):
        """
        Teste get_proxy_for_url sans support PAC.
        """
        # Configurer le mock pour retourner une URL PAC
        mock_detect.return_value = "http://example.com/proxy.pac"
        
        # Simuler l'absence de pypac
        with patch.dict('sys.modules', {'pypac': None}):
            # Forcer l'import à échouer
            if 'pypac' in sys.modules:
                sys.modules.pop('pypac')
            
            # La fonction devrait retourner un dictionnaire vide sans pypac
            result = get_proxy_for_url("http://example.com")
            self.assertEqual(result, {})
    
    @patch('iziproxy.pac_utils._get_pac_proxy')
    def test_get_proxy_for_url_cache(self, mock_get_pac_proxy):
        """
        Teste la mise en cache des résultats PAC.
        """
        # Configuration du mock pour retourner un résultat prédéfini
        expected_proxy = {
            "http": "http://proxy.example.com:8080",
            "https": "http://proxy.example.com:8080"
        }
        mock_get_pac_proxy.return_value = expected_proxy
        
        # Premier appel - utilise la fonction mockée
        result1 = get_proxy_for_url("http://example.com")
        
        # Vérifier que le résultat est correct
        self.assertEqual(result1, expected_proxy)
        mock_get_pac_proxy.assert_called_once()
        
        # Réinitialiser le mock pour le deuxième appel
        mock_get_pac_proxy.reset_mock()
        
        # Deuxième appel - devrait utiliser le cache et ne pas appeler _get_pac_proxy
        result2 = get_proxy_for_url("http://example.com")
        
        # Vérifier que le résultat est identique
        self.assertEqual(result2, expected_proxy)
        
        # Vérifier que la fonction interne n'a pas été appelée car le cache a été utilisé
        mock_get_pac_proxy.assert_not_called()
    
    @unittest.skipIf(sys.platform != "win32", "Test spécifique à Windows")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_detect_system_pac_url_windows(self, mock_query_value, mock_open_key):
        """
        Teste la détection d'URL PAC système sur Windows.
        """
        # Configurer les mocks
        mock_open_key.return_value.__enter__.return_value = MagicMock()
        mock_query_value.return_value = ["http://example.com/proxy.pac", 1]
        
        # Exécuter la détection
        result = detect_system_pac_url()
        
        # Vérifier le résultat
        self.assertEqual(result, "http://example.com/proxy.pac")
    
    @unittest.skipIf(sys.platform != "linux", "Test spécifique à Linux")
    @patch('subprocess.run')
    def test_detect_system_pac_url_linux(self, mock_run):
        """
        Teste la détection d'URL PAC système sur Linux.
        """
        # Configurer le mock
        mock_process = MagicMock()
        mock_process.stdout = "'http://example.com/proxy.pac'"
        mock_run.return_value = mock_process
        
        # Exécuter la détection
        result = detect_system_pac_url()
        
        # Vérifier le résultat
        self.assertEqual(result, "http://example.com/proxy.pac")
    
    def test_clear_pac_cache(self):
        """
        Teste la fonction clear_pac_cache.
        """
        # Forcer une entrée dans le cache
        from iziproxy.pac_utils import _pac_cache
        _pac_cache["test_key"] = (0, {})
        
        # Vérifier que le cache n'est pas vide
        self.assertTrue(bool(_pac_cache))
        
        # Effacer le cache
        clear_pac_cache()
        
        # Vérifier que le cache est vide
        self.assertFalse(bool(_pac_cache))


if __name__ == "__main__":
    unittest.main()
