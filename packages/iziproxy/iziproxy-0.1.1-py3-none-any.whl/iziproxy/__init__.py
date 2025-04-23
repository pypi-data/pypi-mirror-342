from .proxy_ninja import IziProxy
from .pac_utils import get_proxy_for_url, detect_system_pac_url, clear_pac_cache, is_pac_available
from .secure_password import SecureProxyConfig, mask_password_in_url

__all__ = [
    'IziProxy',
    'get_proxy_for_url',
    'detect_system_pac_url',
    'clear_pac_cache',
    'is_pac_available',
    'SecureProxyConfig',
    'mask_password_in_url'
]

__version__ = '0.1.0'