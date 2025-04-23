"""
Tests pour les fonctionnalités de gestion d'identifiants.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
from iziproxy.proxy_ninja import IziProxy


class TestCredentialsManagement(unittest.TestCase):
    """
    Tests unitaires pour la gestion des identifiants de proxy.
    """
    
    def setUp(self):
        """
        Configuration avant chaque test.
        """
        # Sauvegarder les variables d'environnement
        self.original_env = {}
        for key in ['PROXY_USERNAME', 'PROXY_PASSWORD']:
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
    
    @patch('keyring.get_password')
    @patch('keyring.set_password')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_get_credentials_from_keyring(self, mock_input, mock_getpass, 
                                         mock_set_password, mock_get_password):
        """
        Teste la récupération d'identifiants depuis keyring.
        """
        # Configurer les mocks pour simuler des identifiants stockés dans keyring
        mock_get_password.side_effect = lambda service, key: {
            ('iziproxy-local', 'username'): 'stored_user',
            ('iziproxy-local', 'stored_user'): 'stored_pass'
        }.get((service, key))
        
        ninja = IziProxy(environment="local")
        username, password = ninja._get_credentials()
        
        # Vérifier que les identifiants sont récupérés depuis keyring
        self.assertEqual(username, "stored_user")
        self.assertEqual(password, "stored_pass")
        
        # Vérifier que l'interaction utilisateur n'a pas été utilisée
        mock_input.assert_not_called()
        mock_getpass.assert_not_called()
        
        # Vérifier que set_password n'a pas été appelé puisque les identifiants existaient déjà
        mock_set_password.assert_not_called()
    
    @patch('keyring.get_password')
    @patch('keyring.set_password')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_get_credentials_from_env_vars(self, mock_input, mock_getpass, 
                                           mock_set_password, mock_get_password):
        """
        Teste la récupération d'identifiants depuis les variables d'environnement.
        """
        # Configurer les variables d'environnement
        os.environ['PROXY_USERNAME'] = 'env_user'
        os.environ['PROXY_PASSWORD'] = 'env_pass'
        
        # Configurer keyring pour qu'il ne retourne pas d'identifiants
        mock_get_password.return_value = None
        
        ninja = IziProxy()
        username, password = ninja._get_credentials()
        
        # Vérifier que les identifiants sont récupérés depuis les variables d'environnement
        self.assertEqual(username, "env_user")
        self.assertEqual(password, "env_pass")
        
        # Vérifier que l'interaction utilisateur n'a pas été utilisée
        mock_input.assert_not_called()
        mock_getpass.assert_not_called()
        
        # Note: IziProxy stocke les identifiants dans keyring seulement s'ils sont demandés interactivement
        # donc nous ne vérifions pas l'appel à set_password ici
    
    @patch('keyring.get_password')
    @patch('keyring.set_password')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_get_credentials_interactively(self, mock_input, mock_getpass, 
                                           mock_set_password, mock_get_password):
        """
        Teste la récupération interactive d'identifiants.
        """
        # Configurer les mocks pour simuler l'absence d'identifiants dans keyring et env
        mock_get_password.return_value = None
        mock_input.return_value = "interactive_user"
        mock_getpass.return_value = "interactive_pass"
        
        ninja = IziProxy()
        username, password = ninja._get_credentials()
        
        # Vérifier que les identifiants sont récupérés via l'interaction
        self.assertEqual(username, "interactive_user")
        self.assertEqual(password, "interactive_pass")
        
        # Vérifier que l'interaction utilisateur a été utilisée
        mock_input.assert_called_once()
        mock_getpass.assert_called_once()
        
        # Vérifier que les identifiants ont été enregistrés dans keyring
        self.assertEqual(mock_set_password.call_count, 2)  # Un appel pour username, un pour password
    
    @patch('keyring.get_password')
    @patch('keyring.set_password')
    def test_get_credentials_predefined(self, mock_set_password, mock_get_password):
        """
        Teste l'utilisation d'identifiants prédéfinis.
        """
        # Configurer le mock pour simuler l'absence d'identifiants dans keyring
        mock_get_password.return_value = None
        
        ninja = IziProxy()
        username, password = ninja._get_credentials("predefined_user", "predefined_pass")
        
        # Vérifier que les identifiants prédéfinis sont utilisés
        self.assertEqual(username, "predefined_user")
        self.assertEqual(password, "predefined_pass")
        
        # Note: IziProxy stocke les identifiants dans keyring seulement s'ils sont demandés interactivement
        # donc nous ne vérifions pas l'appel à set_password ici


if __name__ == "__main__":
    unittest.main()