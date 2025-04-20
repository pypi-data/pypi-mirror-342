from .http import HttpClient
from .keys import Keys


class HkJingXiuBilling:
    def __init__(self, base_url: str, admin_key: str = None):
        self.base_url = base_url
        self.http_client = HttpClient(base_url=base_url, key=admin_key)
        self.keys = Keys(self.http_client)

    def set_admin_key(self, admin_key: str) -> None:
        """设置管理密钥

        Args:
            admin_key: 管理密钥
        """
        self.keys.set_admin_key(admin_key)


__all__ = ["HkJingXiuBilling"]
