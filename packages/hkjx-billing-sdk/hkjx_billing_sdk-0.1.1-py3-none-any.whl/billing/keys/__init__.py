from ..http import HttpClient
from .schemas import (
    KeyConsumeRequest,
    KeyConsumeResponse,
    KeyCreate,
    KeyResponse,
    KeyVerifyResponse,
)


class Keys:
    """密钥管理类."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    async def create_key(self, key_create: KeyCreate) -> KeyResponse:
        """创建密钥.

        Args:
            key_create: 创建密钥请求

        Returns:
            KeyResponse: 密钥响应
        """
        response = await self.client.post("/keys", json=key_create)
        return KeyResponse(**response["data"])

    async def verify_key(self, key_id: str) -> KeyVerifyResponse:
        """验证密钥.

        Args:
            verify_request: 验证密钥请求

        Returns:
            KeyVerifyResponse: 验证密钥响应
        """
        response = await self.client.post("/keys/verify?key=" + key_id)
        return KeyVerifyResponse(**response["data"])

    async def consume_key(
        self, consume_request: KeyConsumeRequest
    ) -> KeyConsumeResponse:
        """消费密钥.

        Args:
            consume_request: 消费密钥请求

        Returns:
            KeyConsumeResponse: 消费密钥响应
        """
        response = await self.client.post("/keys/consume", json=consume_request)
        return KeyConsumeResponse(**response["data"])


__all__ = [
    "Keys",
    "KeyCreate",
    "KeyResponse",
    "KeyVerifyResponse",
    "KeyConsumeRequest",
    "KeyConsumeResponse",
]
