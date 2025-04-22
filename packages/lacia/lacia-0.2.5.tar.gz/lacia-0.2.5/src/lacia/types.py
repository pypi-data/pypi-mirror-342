from __future__ import annotations

from enum import Enum
from contextvars import ContextVar
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from lacia.standard.abcbase import Namespace

Message = Dict[str, Any]

class JsonRpcCode(int, Enum):
    ParseError = -32700             
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerError = -32000
    StopAsyncIterationError = -32099

class RpcMessage:

    def __init__(self, data: Dict[str, Any]):
        self.data = data
    
    @property
    def jsonrpc(self) -> str:
        return self.data.get("jsonrpc", None)
    
    @property
    def id(self) -> Any:
        return self.data.get("id", None)

    @property
    def method(self):
        return self.data.get("method", {})

    @property
    def result(self) -> Any:
        return self.data.get("result", None)
    
    @property
    def error(self) -> Any:
        return self.data.get("error", None)
    
    @property
    def error_code(self) -> int:
        return self.data["error"]["code"]

    @property
    def error_msg(self) -> str:
        return self.data["error"]["message"]
    
    @property
    def is_error(self) -> bool:
        return "error" in self.data

    @property
    def is_request(self) -> bool:
        return "method" in self.data
    
    @property
    def is_response(self) -> bool:
        return "result" in self.data or "error" in self.data


class Context:
    websocket: ContextVar = ContextVar("websocket")
    name: ContextVar[str] = ContextVar("name")
    token: ContextVar[str] = ContextVar("token")
    namespace: ContextVar[Namespace] = ContextVar("namespace")
    rpc: ContextVar = ContextVar("rpc")
    headers: ContextVar[dict[str, Any]] = ContextVar("headers")

    @classmethod
    def get_cookie(cls) -> dict[str, Any]:
        headers = cls.headers.get()
        if headers is None:
            return {}
        cookie = headers.get("cookie", {})
        return {
            k: v for k, v in (item.split("=", 1) for item in cookie.split("; "))
        }
