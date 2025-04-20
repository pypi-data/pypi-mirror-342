from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


# Key 相关模型
class KeyCreate(BaseModel):
    """创建密钥请求"""

    user_id: Optional[str] = Field(default=None, description="用户ID", example="user1")
    service_code: str = Field(..., description="服务代码", example="ADM")
    credit_limit: Optional[float] = Field(
        default=None, description="额度限制", example=1000.0
    )
    expires_at: Optional[datetime] = Field(
        default=None, description="过期时间", example=datetime.now()
    )


class KeyResponse(BaseModel):
    """密钥响应"""

    id: str
    app_id: str
    user_id: str
    service_id: int
    credit_limit: float
    credit_used: float
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class KeyVerifyResponse(BaseModel):
    """验证密钥响应"""

    valid: bool = Field(..., description="是否有效")
    key_id: Optional[str] = Field(None, description="密钥ID")
    credit_limit: Optional[float] = Field(None, description="额度限制")
    credit_used: Optional[float] = Field(None, description="已使用额度")
    credit_available: Optional[float] = Field(None, description="可用额度")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class KeyConsumeRequest(BaseModel):
    """消费密钥请求"""

    key_id: str = Field(..., description="密钥ID")
    amount: float = Field(..., description="消费数量")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class KeyConsumeResponse(BaseModel):
    """消费密钥响应"""

    success: bool = Field(..., description="是否成功")
    key_id: str = Field(..., description="密钥ID")
    amount: float = Field(..., description="消费数量")
    credit_used: float = Field(..., description="已使用额度")
    credit_available: float = Field(..., description="可用额度")
