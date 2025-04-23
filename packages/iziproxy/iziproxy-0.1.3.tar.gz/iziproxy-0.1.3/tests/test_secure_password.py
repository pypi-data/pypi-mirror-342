"""
Tests pour le module secure_password.
"""

import unittest
from iziproxy.secure_password import SecureProxyConfig, mask_password_in_url


class TestSecurePassword(unittest.TestCase):
    """
    Tests unitaires pour les fonctionnalités de masquage de mots de passe.
    """
    
    def test_mask_password_in_url(self):
        """
        Teste la fonction de masquage de mot de passe dans une URL.
        """
        # Test avec URL contenant un mot de passe
        url = "http://user:password123@example.com:8080"
        masked = mask_password_in_url(url)
        self.assertEqual(masked, "http://user:********@example.com:8080")
        
        # Test avec URL sans mot de passe
        url = "http://example.com:8080"
        masked = mask_password_in_url(url)
        self.assertEqual(masked, url)
        
        # Test avec URL None
        masked = mask_password_in_url(None)
        self.assertEqual(masked, "")
    
    def test_secure_proxy_config_init(self):
        """
        Teste l'initialisation de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier que la configuration interne est correcte
        self.assertEqual(secure_config.get_config(), config)
    
    def test_secure_proxy_config_str(self):
        """
        Teste la représentation string de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier que le mot de passe est masqué dans la représentation string
        str_repr = str(secure_config)
        self.assertIn("********", str_repr)
        self.assertNotIn("password123", str_repr)
    
    def test_secure_proxy_config_repr(self):
        """
        Teste la représentation repr de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier que le mot de passe est masqué dans la représentation repr
        repr_str = repr(secure_config)
        self.assertIn("********", repr_str)
        self.assertNotIn("password123", repr_str)
        self.assertTrue(repr_str.startswith("SecureProxyConfig("))
    
    def test_secure_proxy_config_getitem(self):
        """
        Teste l'accès aux éléments de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier l'accès via []
        self.assertEqual(secure_config["http"], config["http"])
        self.assertEqual(secure_config["https"], config["https"])
    
    def test_secure_proxy_config_contains(self):
        """
        Teste l'opération 'in' sur SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier l'opération 'in'
        self.assertTrue("http" in secure_config)
        self.assertTrue("https" in secure_config)
        self.assertFalse("ftp" in secure_config)
    
    def test_secure_proxy_config_get(self):
        """
        Teste la méthode get de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier la méthode get
        self.assertEqual(secure_config.get("http"), config["http"])
        self.assertEqual(secure_config.get("ftp", "default"), "default")
    
    def test_secure_proxy_config_dict_methods(self):
        """
        Teste les méthodes dictionnaire de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier les méthodes dictionnaire
        self.assertEqual(set(secure_config.keys()), set(config.keys()))
        self.assertEqual(set(secure_config.values()), set(config.values()))
        self.assertEqual(set(tuple(x) for x in secure_config.items()), 
                         set(tuple(x) for x in config.items()))
    
    def test_secure_proxy_config_copy(self):
        """
        Teste la méthode copy de SecureProxyConfig.
        """
        config = {
            "http": "http://user:password123@proxy.example.com:8080",
            "https": "http://user:password123@proxy.example.com:8080"
        }
        secure_config = SecureProxyConfig(config)
        
        # Vérifier la méthode copy
        config_copy = secure_config.copy()
        self.assertEqual(config_copy, config)
        self.assertIsNot(config_copy, config)


if __name__ == "__main__":
    unittest.main()
