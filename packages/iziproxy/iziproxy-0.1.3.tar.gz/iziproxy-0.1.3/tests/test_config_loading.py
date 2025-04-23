"""
Tests pour le chargement et l'utilisation de fichiers de configuration.
"""

import unittest
from unittest.mock import patch, mock_open
import os
import tempfile
from iziproxy.proxy_ninja import IziProxy


class TestConfigLoading(unittest.TestCase):
    """
    Tests unitaires pour le chargement de configuration.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Contenu pour les tests
        self.yaml_content = """
        environments:
          local:
            proxy_url: http://proxy.local.example.com:8080
            requires_auth: true
          dev:
            proxy_url: http://proxy.dev.example.com:8080
            requires_auth: true
          prod:
            proxy_url: http://proxy.prod.example.com:8080
            requires_auth: false
        
        environment_detection:
          method: hostname
          hostname_patterns:
            local: ["laptop", "dev-pc"]
            dev: ["dev-server"]
            prod: ["prod-server"]
        """
    
    def test_load_config_file_explicit(self):
        """
        Teste le chargement d'un fichier de configuration explicite.
        """
        # Utiliser mock_open pour simuler un fichier
        with patch('builtins.open', mock_open(read_data=self.yaml_content)):
            ninja = IziProxy(config_file="explicit_config.yaml")
            
            # Vérifier que la configuration a été chargée correctement
            self.assertIn("environments", ninja.config)
            self.assertIn("local", ninja.config["environments"])
            self.assertIn("dev", ninja.config["environments"])
            self.assertIn("prod", ninja.config["environments"])
            
            # Vérifier les details de configuration
            self.assertEqual(
                ninja.config["environments"]["local"]["proxy_url"],
                "http://proxy.local.example.com:8080"
            )
            self.assertTrue(ninja.config["environments"]["local"]["requires_auth"])
            self.assertFalse(ninja.config["environments"]["prod"]["requires_auth"])
    
    def test_load_config_file_default_locations(self):
        """
        Teste le chargement d'un fichier de configuration depuis les emplacements par défaut.
        """
        # Mock pour os.path.exists pour simuler l'existence du fichier
        with patch('os.path.exists', return_value=True):
            # Mock pour open pour simuler le contenu du fichier
            with patch('builtins.open', mock_open(read_data=self.yaml_content)):
                ninja = IziProxy()
                
                # Vérifier que la configuration a été chargée correctement
                self.assertIn("environments", ninja.config)
                self.assertIn("environment_detection", ninja.config)
    
    def test_load_config_file_real(self):
        """
        Teste le chargement d'un fichier de configuration réel.
        """
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.yaml') as temp_file:
            temp_file.write(self.yaml_content)
            temp_file_path = temp_file.name
        
        try:
            # Charger la configuration depuis le fichier temporaire
            ninja = IziProxy(config_file=temp_file_path)
            
            # Vérifier que la configuration a été chargée correctement
            self.assertIn("environments", ninja.config)
            self.assertEqual(
                ninja.config["environments"]["dev"]["proxy_url"],
                "http://proxy.dev.example.com:8080"
            )
        finally:
            # Supprimer le fichier temporaire
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    def test_load_config_file_invalid(self):
        """
        Teste la gestion des erreurs lors du chargement d'un fichier de configuration invalide.
        """
        # Contenu YAML invalide
        invalid_yaml = """
        environments:
          local:
            proxy_url: http://proxy.local.example.com:8080
          - invalid indentation
        """
        
        # Utiliser mock_open pour simuler un fichier invalide
        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            # Décorator pour capturer les logs d'avertissement
            with self.assertLogs(level='WARNING') as log_context:
                ninja = IziProxy(config_file="invalid_config.yaml")
                
                # Vérifier que la configuration est un dict vide à cause de l'erreur
                self.assertEqual(ninja.config, {})
                
                # Vérifier qu'un avertissement a été enregistré
                self.assertTrue(any("Erreur lors du chargement" in log for log in log_context.output))
    
    def test_load_config_file_nonexistent(self):
        """
        Teste la gestion des erreurs lors du chargement d'un fichier non existant.
        """
        # Utiliser un fichier qui n'existe pas
        with patch('os.path.exists', return_value=False):
            ninja = IziProxy(config_file="nonexistent_config.yaml")
            
            # Vérifier que la configuration est un dict vide
            self.assertEqual(ninja.config, {})
    
    def test_environment_config_usage(self):
        """
        Teste l'utilisation des configurations spécifiques à l'environnement.
        """
        # Utiliser mock_open pour simuler un fichier
        with patch('builtins.open', mock_open(read_data=self.yaml_content)):
            # Créer une instance avec un environnement spécifique
            ninja = IziProxy(config_file="config.yaml", environment="dev")
            
            # Vérifier que l'environnement est utilisé correctement
            self.assertEqual(ninja.environment, "dev")
            
            # Simuler l'obtention d'une configuration de proxy
            with patch.object(ninja, '_get_env_proxy_config', return_value={}):
                with patch.object(ninja, '_get_credentials', return_value=("user", "pass")):
                    config = ninja.get_proxy_config()
                    
                    # Vérifier que la configuration de l'environnement dev est utilisée
                    config_str = str(config)
                    self.assertIn("proxy.dev.example.com", config_str)
                    self.assertIn("user", config_str)


if __name__ == "__main__":
    unittest.main()